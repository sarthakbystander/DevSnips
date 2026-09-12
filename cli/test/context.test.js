/**
 * Tests for DevSnips CLI project-context orchestration.
 *
 * Verifies initializeContext / updateContextAfterInstall / isContextInitialized
 * behavior: fresh initialization, preservation of existing files, safe failure
 * on malformed config, and success-only installation recording.
 *
 * Run with: node test/context.test.js
 */

const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const {
  initializeContext,
  updateContextAfterInstall,
  isContextInitialized
} = require('../src/devsnips/context.js');
const {
  readConfig,
  getConfigPath
} = require('../src/devsnips/config.js');
const { readAgents, getAgentsPath } = require('../src/devsnips/agents.js');

let testDir;
let originalCwd;

function setup() {
  testDir = fs.mkdtempSync(path.join(os.tmpdir(), 'devsnips-context-test-'));
  originalCwd = process.cwd();
  process.chdir(testDir);
}

function teardown() {
  process.chdir(originalCwd);
  try {
    fs.rmSync(testDir, { recursive: true, force: true });
  } catch (e) {
    // Ignore cleanup errors
  }
}

function check(name, fn) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
  } catch (error) {
    console.error(`  ✗ ${name}`);
    console.error(`    ${error.message}`);
    throw error;
  }
}

// Fresh initialization creates the directory, config.json, and AGENTS.md
check('initializeContext creates full project context', () => {
  setup();
  const result = initializeContext();

  assert.strictEqual(result.agentsCreated, true);
  assert.strictEqual(result.configCreated, true);
  assert.ok(fs.existsSync(path.join(process.cwd(), 'devsnips')));
  assert.ok(fs.existsSync(getConfigPath()));
  assert.ok(fs.existsSync(getAgentsPath()));

  const config = readConfig();
  assert.strictEqual(config.version, 1);
  assert.deepStrictEqual(config.resources, []);
  teardown();
});

// isContextInitialized reflects actual state
check('isContextInitialized reflects actual state', () => {
  setup();
  assert.strictEqual(isContextInitialized(), false);
  initializeContext();
  assert.strictEqual(isContextInitialized(), true);
  teardown();
});

// initializeContext never overwrites a user-customized AGENTS.md
check('initializeContext preserves custom AGENTS.md', () => {
  setup();
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  fs.mkdirSync(devsnipsDir, { recursive: true });
  const agentsPath = getAgentsPath();
  const customContent = '# My custom agent instructions\n\nProject-specific.\n';
  fs.writeFileSync(agentsPath, customContent, 'utf8');

  const result = initializeContext();
  assert.strictEqual(result.agentsCreated, false);
  assert.strictEqual(readAgents(), customContent);
  teardown();
});

// initializeContext preserves an existing valid config
check('initializeContext preserves existing config', () => {
  setup();
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  fs.mkdirSync(devsnipsDir, { recursive: true });
  const existing = { version: 1, project: { framework: 'react' }, resources: [] };
  fs.writeFileSync(getConfigPath(), JSON.stringify(existing, null, 2) + '\n', 'utf8');

  const result = initializeContext();
  assert.strictEqual(result.configCreated, false);
  assert.deepStrictEqual(readConfig().project, { framework: 'react' });
  teardown();
});

// initializeContext fails safely on malformed config and leaves it untouched
check('initializeContext fails safely on malformed config', () => {
  setup();
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  fs.mkdirSync(devsnipsDir, { recursive: true });
  const malformed = '{ this is not json ]';
  fs.writeFileSync(getConfigPath(), malformed, 'utf8');

  assert.throws(() => initializeContext(), /invalid JSON|config\.json/i);

  // File must remain byte-for-byte untouched
  assert.strictEqual(fs.readFileSync(getConfigPath(), 'utf8'), malformed);
  teardown();
});

// updateContextAfterInstall records an installation in config
check('updateContextAfterInstall records an installation', () => {
  setup();
  initializeContext();
  updateContextAfterInstall('Tailwind/Components/Buttons/solid-button', 'Tailwind CSS');

  const config = readConfig();
  assert.strictEqual(config.resources.length, 1);
  assert.strictEqual(config.resources[0].path, 'Tailwind/Components/Buttons/solid-button');
  assert.strictEqual(config.resources[0].technology, 'Tailwind CSS');
  assert.ok(config.resources[0].installedAt);
  teardown();
});

// updateContextAfterInstall does not create duplicates
check('updateContextAfterInstall does not create duplicates', () => {
  setup();
  initializeContext();
  updateContextAfterInstall('Vanilla/Components/Buttons/split-button', 'Vanilla HTML/CSS/JS');
  const second = updateContextAfterInstall('Vanilla/Components/Buttons/split-button', 'Vanilla HTML/CSS/JS');

  assert.strictEqual(second, false);
  assert.strictEqual(readConfig().resources.length, 1);
  teardown();
});

// Recording only happens when the caller invokes it after a successful install:
// initializing context alone must never fabricate an installation record.
check('initialization alone does not record any installation', () => {
  setup();
  initializeContext();
  assert.deepStrictEqual(readConfig().resources, []);
  teardown();
});

// Atomic config writes leave no temporary files behind
check('config writes leave no .tmp files behind', () => {
  setup();
  initializeContext();
  updateContextAfterInstall('React/Components/Buttons/solid-button', 'React');

  const devsnipsDirFS = fs.readdirSync(path.join(process.cwd(), 'devsnips'));
  assert.ok(!devsnipsDirFS.some(f => f.endsWith('.tmp')));
  teardown();
});

console.log('\nAll context tests passed\n');
