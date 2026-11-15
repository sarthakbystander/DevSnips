/**
 * Tests for DevSnips CLI file writer
 *
 * Run with: node test/writer.test.js
 */

const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const {
  writeFile,
  calculateDestination,
  getDestinationFilePath
} = require('../src/install/writer.js');

let testDir;
let originalCwd;
let exitCalls;
let exitMessages;

function setup() {
  // Create isolated temp directory
  testDir = fs.mkdtempSync(path.join(os.tmpdir(), 'devsnips-writer-test-'));
  originalCwd = process.cwd();
  process.chdir(testDir);
  exitCalls = [];
  exitMessages = [];

  // Stub process.exit and console.error so exit paths can be asserted
  // instead of terminating the test process or polluting test output.
  const originalExit = process.exit;
  const originalConsoleError = console.error;
  process.exit = (code) => {
    exitCalls.push(code);
    throw new Error(`__process_exit_${code}__`);
  };
  console.error = (...parts) => {
    exitMessages.push(parts.join(' '));
  };
  return () => {
    process.exit = originalExit;
    console.error = originalConsoleError;
  };
}

function restore() {
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

// --- writeFile: security guard ---

check('writeFile writes inside the devsnips directory', () => {
  const restoreExit = setup();
  try {
    const target = path.join(testDir, 'devsnips', 'tailwind', 'code.html');
    const result = writeFile(target, '<p>hello</p>');
    assert.strictEqual(result, true);
    assert.strictEqual(fs.readFileSync(target, 'utf8'), '<p>hello</p>');
    assert.deepStrictEqual(exitCalls, []);
  } finally {
    restoreExit();
    restore();
  }
});

check('writeFile refuses to write outside the devsnips directory', () => {
  const restoreExit = setup();
  try {
    const target = path.join(testDir, 'escaped', 'code.html');
    assert.throws(
      () => writeFile(target, 'x'),
      /__process_exit_1__/
    );
    assert.deepStrictEqual(exitCalls, [1]);
    assert.ok(exitMessages.join(' ').includes('Security violation'));
    assert.strictEqual(fs.existsSync(target), false);
  } finally {
    restoreExit();
    restore();
  }
});

check('writeFile refuses sibling directories that share a name prefix', () => {
  const restoreExit = setup();
  try {
    const target = path.join(testDir, 'devsnips-evil', 'code.html');
    assert.throws(
      () => writeFile(target, 'x'),
      /__process_exit_1__/
    );
    assert.deepStrictEqual(exitCalls, [1]);
    assert.ok(exitMessages.join(' ').includes('Security violation'));
  } finally {
    restoreExit();
    restore();
  }
});

// --- writeFile: overwrite behavior ---

check('writeFile exits when the file already exists and allowOverwrite is false', () => {
  const restoreExit = setup();
  try {
    const target = path.join(testDir, 'devsnips', 'react', 'code.html');
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, 'original');

    assert.throws(
      () => writeFile(target, 'new content'),
      /__process_exit_1__/
    );
    assert.deepStrictEqual(exitCalls, [1]);
    assert.strictEqual(fs.readFileSync(target, 'utf8'), 'original');
  } finally {
    restoreExit();
    restore();
  }
});

check('writeFile overwrites when allowOverwrite is true (--force)', () => {
  const restoreExit = setup();
  try {
    const target = path.join(testDir, 'devsnips', 'react', 'code.html');
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, 'original');

    const result = writeFile(target, 'new content', true);
    assert.strictEqual(result, true);
    assert.strictEqual(fs.readFileSync(target, 'utf8'), 'new content');
    assert.deepStrictEqual(exitCalls, []);
  } finally {
    restoreExit();
    restore();
  }
});

// --- calculateDestination ---

check('calculateDestination strips the leading tech segment and lowercases', () => {
  const restoreExit = setup();
  try {
    const dest = calculateDestination(
      'Tailwind/Sections/AI-Product/agent-workflow/vercel',
      'Tailwind CSS'
    );
    assert.strictEqual(
      dest,
      path.join(testDir, 'devsnips', 'tailwind', 'sections', 'ai-product', 'agent-workflow', 'vercel')
    );
  } finally {
    restoreExit();
    restore();
  }
});

check('calculateDestination handles trailing slashes and React paths', () => {
  const restoreExit = setup();
  try {
    const dest = calculateDestination('React/Components/Buttons/solid-button/', 'React');
    assert.strictEqual(
      dest,
      path.join(testDir, 'devsnips', 'react', 'components', 'buttons', 'solid-button')
    );
  } finally {
    restoreExit();
    restore();
  }
});

check('calculateDestination maps Vanilla technology names and bare tech paths', () => {
  const restoreExit = setup();
  try {
    assert.strictEqual(
      calculateDestination('Vanilla/Components/Tooltips/tooltip', 'Vanilla HTML/CSS/JS'),
      path.join(testDir, 'devsnips', 'vanilla', 'components', 'tooltips', 'tooltip')
    );
    // A path that is only the tech segment leaves just the slug
    assert.strictEqual(
      calculateDestination('Vanilla', 'Vanilla HTML/CSS/JS'),
      path.join(testDir, 'devsnips', 'vanilla')
    );
  } finally {
    restoreExit();
    restore();
  }
});

// --- getDestinationFilePath ---

check('getDestinationFilePath joins destDir with the filename', () => {
  const destDir = path.join('devsnips', 'react', 'components');
  assert.strictEqual(
    getDestinationFilePath(destDir, 'code.tsx'),
    path.join(destDir, 'code.tsx')
  );
});

console.log('writer.test.js: all checks passed');
