/**
 * Offline end-to-end tests for the `add` command flow
 *
 * Uses the DEVSNIPS_REGISTRY_URL / DEVSNIPS_RAW_BASE environment overrides
 * to point the CLI at a local HTTP fixture server, so the full flow
 * (registry fetch -> resolve -> download -> write -> context update) and its
 * --dry-run variant run with no network access.
 *
 * The command runs in-process (process.exit and console are stubbed the same
 * way writer.test.js does) rather than via a spawned child: some dev/CI
 * sandboxes intercept loopback TCP between processes, which makes a local
 * fixture server unreachable from a child. Argument wiring is covered by the
 * parseAddCommand unit tests.
 *
 * Run with: node --test
 */

const { test, before, after } = require('node:test');
const assert = require('node:assert');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const { parseAddCommand } = require('../src/utils/args.js');
const { runAddCommand } = require('../src/commands/add.js');

const CANONICAL = 'Vanilla/Components/Buttons/split-button';

const REGISTRY = {
  families: [
    {
      name: 'Buttons',
      tech: 'Vanilla HTML/CSS/JS',
      type: 'component',
      category: 'Components',
      variants: [
        {
          path: CANONICAL,
          type: 'component',
          files: ['code.html']
        }
      ]
    }
  ]
};

const CODE_HTML = '<!-- fixture -->\n<div class="btn-group"><button>Action</button></div>\n';

let server;
let baseUrl;

before(async () => {
  server = http.createServer((req, res) => {
    if (req.url === '/snippets-index.json') {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify(REGISTRY));
      return;
    }
    if (req.url === `/library/${CANONICAL}/code.html`) {
      // text/plain, not text/html: the downloader rejects HTML responses
      res.writeHead(200, { 'content-type': 'text/plain' });
      res.end(CODE_HTML);
      return;
    }
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end('not found');
  });
  await new Promise((resolve) => {
    server.listen(0, '127.0.0.1', resolve);
  });
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(() => {
  if (server) {
    server.close();
  }
});

// --- parseAddCommand (pure argument wiring) ---

test('parseAddCommand extracts path and flags', () => {
  assert.deepStrictEqual(
    parseAddCommand(['React/Components/Buttons/solid-button', '--force', '--dry-run']),
    { componentPath: 'React/Components/Buttons/solid-button', force: true, dryRun: true }
  );
  assert.deepStrictEqual(
    parseAddCommand(['Vanilla/Components/Buttons/split-button']),
    { componentPath: 'Vanilla/Components/Buttons/split-button', force: false, dryRun: false }
  );
});

test('parseAddCommand rejects a missing path', () => {
  assert.deepStrictEqual(parseAddCommand(['--force', '--dry-run']), { error: 'missing-path' });
  assert.deepStrictEqual(parseAddCommand([]), { error: 'missing-path' });
});

// --- full flow against the fixture server, in-process ---

function makeTempProject() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'devsnips-e2e-'));
}

async function runAddInProcess(cwd, extraArgs) {
  const previousCwd = process.cwd();
  const hadRegistryUrl = Object.prototype.hasOwnProperty.call(process.env, 'DEVSNIPS_REGISTRY_URL');
  const hadRawBase = Object.prototype.hasOwnProperty.call(process.env, 'DEVSNIPS_RAW_BASE');
  const previousRegistryUrl = process.env.DEVSNIPS_REGISTRY_URL;
  const previousRawBase = process.env.DEVSNIPS_RAW_BASE;

  process.chdir(cwd);
  process.env.DEVSNIPS_REGISTRY_URL = `${baseUrl}/snippets-index.json`;
  // NOTE: no /library/ suffix here - buildRepoFilePath() already prepends
  // "library/" to each requested path, exactly as with the GitHub raw base.
  process.env.DEVSNIPS_RAW_BASE = `${baseUrl}/`;

  const previousExit = process.exit;
  const previousLog = console.log;
  const lines = [];
  let exitCode = null;

  process.exit = (code) => {
    exitCode = code;
    throw new Error('__process_exit__');
  };
  console.log = (...parts) => {
    lines.push(parts.join(' '));
  };

  try {
    await runAddCommand(CANONICAL, {
      force: extraArgs.includes('--force'),
      dryRun: extraArgs.includes('--dry-run')
    });
  } catch (error) {
    if (error.message !== '__process_exit__') {
      process.exit = previousExit;
      console.log = previousLog;
      process.chdir(previousCwd);
      throw error;
    }
  } finally {
    process.exit = previousExit;
    console.log = previousLog;
    process.chdir(previousCwd);
    if (hadRegistryUrl) {
      process.env.DEVSNIPS_REGISTRY_URL = previousRegistryUrl;
    } else {
      delete process.env.DEVSNIPS_REGISTRY_URL;
    }
    if (hadRawBase) {
      process.env.DEVSNIPS_RAW_BASE = previousRawBase;
    } else {
      delete process.env.DEVSNIPS_RAW_BASE;
    }
  }

  return { exitCode, output: lines.join('\n') };
}

test('add --dry-run resolves and reports without writing anything', async () => {
  const cwd = makeTempProject();
  try {
    const { exitCode, output } = await runAddInProcess(cwd, ['--dry-run']);

    assert.strictEqual(exitCode, 0, output);
    assert.ok(output.includes('Dry run complete'), output);
    assert.ok(output.includes('Would install to:'), output);
    assert.ok(output.includes('- code.html'), output);

    // Nothing was written: no devsnips directory, no component files
    assert.deepStrictEqual(fs.readdirSync(cwd), []);
  } finally {
    fs.rmSync(cwd, { recursive: true, force: true });
  }
});

test('add installs fully offline via the env overrides', async () => {
  const cwd = makeTempProject();
  try {
    const { exitCode, output } = await runAddInProcess(cwd, []);

    assert.strictEqual(exitCode, 0, output);

    const codeFile = path.join(
      cwd, 'devsnips', 'vanilla', 'components', 'buttons', 'split-button', 'code.html'
    );
    assert.ok(fs.existsSync(codeFile), 'code.html not installed at expected destination');
    assert.strictEqual(fs.readFileSync(codeFile, 'utf8'), CODE_HTML);

    // Project context was initialized and the install recorded
    const configFile = path.join(cwd, 'devsnips', 'config.json');
    assert.ok(fs.existsSync(configFile), 'config.json not created');
    const config = JSON.parse(fs.readFileSync(configFile, 'utf8'));
    assert.ok(JSON.stringify(config).includes(CANONICAL), 'install not recorded in config.json');
  } finally {
    fs.rmSync(cwd, { recursive: true, force: true });
  }
});

test('add --force overwrites an existing installation cleanly', async () => {
  const cwd = makeTempProject();
  try {
    assert.strictEqual((await runAddInProcess(cwd, ['--force'])).exitCode, 0, 'first install failed');
    assert.strictEqual((await runAddInProcess(cwd, ['--force'])).exitCode, 0, '--force reinstall failed');

    const codeFile = path.join(
      cwd, 'devsnips', 'vanilla', 'components', 'buttons', 'split-button', 'code.html'
    );
    assert.strictEqual(fs.readFileSync(codeFile, 'utf8'), CODE_HTML);

    // Recorded exactly once in the project context
    const config = JSON.parse(fs.readFileSync(path.join(cwd, 'devsnips', 'config.json'), 'utf8'));
    const recorded = JSON.stringify(config).split(CANONICAL).length - 1;
    assert.ok(recorded <= 1, `resource recorded ${recorded} times in config.json`);
  } finally {
    fs.rmSync(cwd, { recursive: true, force: true });
  }
});

test('add --dry-run after a real install does not overwrite or re-record', async () => {
  const cwd = makeTempProject();
  try {
    assert.strictEqual((await runAddInProcess(cwd, [])).exitCode, 0, 'real install failed');

    const configPath = path.join(cwd, 'devsnips', 'config.json');
    const configBefore = fs.readFileSync(configPath, 'utf8');
    const { exitCode } = await runAddInProcess(cwd, ['--dry-run']);

    assert.strictEqual(exitCode, 0);
    assert.strictEqual(
      fs.readFileSync(configPath, 'utf8'),
      configBefore,
      'config.json changed during dry run'
    );
  } finally {
    fs.rmSync(cwd, { recursive: true, force: true });
  }
});
