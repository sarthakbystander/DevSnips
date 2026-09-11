/**
 * Tests for DevSnips CLI config management
 *
 * Run with: node test/config.test.js
 */

const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const {
  getConfigPath,
  ensureDevSnipsDirectory,
  createDefaultConfig,
  readConfig,
  writeConfig,
  ensureConfig,
  recordInstallation,
  isResourceInstalled
} = require('../src/devsnips/config.js');

let testDir;
let originalCwd;

function setup() {
  // Create isolated temp directory
  testDir = fs.mkdtempSync(path.join(os.tmpdir(), 'devsnips-test-'));
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

// Test: createDefaultConfig returns correct structure
check('createDefaultConfig returns correct structure', () => {
  const config = createDefaultConfig();
  assert.strictEqual(config.version, 1);
  assert.deepStrictEqual(config.project, {});
  assert.deepStrictEqual(config.resources, []);
});

// Test: getConfigPath returns correct path
check('getConfigPath returns correct path', () => {
  const configPath = getConfigPath();
  const expected = path.join(process.cwd(), 'devsnips', 'config.json');
  assert.strictEqual(configPath, expected);
});

// Test: ensureDevSnipsDirectory creates directory
check('ensureDevSnipsDirectory creates devsnips directory', () => {
  setup();
  ensureDevSnipsDirectory();
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  assert.ok(fs.existsSync(devsnipsDir));
  teardown();
});

// Test: readConfig returns null when file does not exist
check('readConfig returns null when file does not exist', () => {
  setup();
  const config = readConfig();
  assert.strictEqual(config, null);
  teardown();
});

// Test: readConfig parses valid JSON
check('readConfig parses valid JSON', () => {
  setup();
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  fs.mkdirSync(devsnipsDir, { recursive: true });
  const configPath = path.join(devsnipsDir, 'config.json');
  fs.writeFileSync(configPath, JSON.stringify({ version: 1, project: {}, resources: [] }, null, 2) + '\n');
  
  const config = readConfig();
  assert.strictEqual(config.version, 1);
  teardown();
});

// Test: readConfig throws on malformed JSON
check('readConfig throws on malformed JSON', () => {
  setup();
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  fs.mkdirSync(devsnipsDir, { recursive: true });
  const configPath = path.join(devsnipsDir, 'config.json');
  fs.writeFileSync(configPath, '{ invalid json }');
  
  assert.throws(() => readConfig(), /invalid JSON/i);
  teardown();
});

// Test: writeConfig writes formatted JSON
check('writeConfig writes formatted JSON', () => {
  setup();
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  fs.mkdirSync(devsnipsDir, { recursive: true });
  const configPath = path.join(devsnipsDir, 'config.json');
  
  const config = { version: 1, project: {}, resources: [{ path: 'Test/Component' }] };
  writeConfig(config);
  
  const content = fs.readFileSync(configPath, 'utf8');
  assert.ok(content.includes('  "version": 1')); // 2-space indentation
  assert.ok(content.endsWith('\n')); // trailing newline
  teardown();
});

// Test: ensureConfig creates config if missing
check('ensureConfig creates config if missing', () => {
  setup();
  const config = ensureConfig();
  assert.strictEqual(config.version, 1);
  assert.deepStrictEqual(config.resources, []);
  
  const configPath = getConfigPath();
  assert.ok(fs.existsSync(configPath));
  teardown();
});

// Test: ensureConfig reads existing config
check('ensureConfig reads existing config', () => {
  setup();
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  fs.mkdirSync(devsnipsDir, { recursive: true });
  const configPath = path.join(devsnipsDir, 'config.json');
  const existingConfig = { version: 1, project: { framework: 'react' }, resources: [] };
  fs.writeFileSync(configPath, JSON.stringify(existingConfig, null, 2) + '\n');
  
  const config = ensureConfig();
  assert.deepStrictEqual(config.project, { framework: 'react' });
  teardown();
});

// Test: recordInstallation adds new record
check('recordInstallation adds new record', () => {
  setup();
  const result = recordInstallation('Vanilla/Components/Buttons/split-button', 'Vanilla HTML/CSS/JS');
  assert.strictEqual(result, true);
  
  const config = readConfig();
  assert.strictEqual(config.resources.length, 1);
  assert.strictEqual(config.resources[0].path, 'Vanilla/Components/Buttons/split-button');
  assert.strictEqual(config.resources[0].technology, 'Vanilla HTML/CSS/JS');
  assert.ok(config.resources[0].installedAt);
  teardown();
});

// Test: recordInstallation does not duplicate
check('recordInstallation does not duplicate existing records', () => {
  setup();
  recordInstallation('Vanilla/Components/Buttons/split-button', 'Vanilla HTML/CSS/JS');
  const result = recordInstallation('Vanilla/Components/Buttons/split-button', 'Vanilla HTML/CSS/JS');
  assert.strictEqual(result, false);
  
  const config = readConfig();
  assert.strictEqual(config.resources.length, 1);
  teardown();
});

// Test: isResourceInstalled returns correct values
check('isResourceInstalled returns correct values', () => {
  setup();
  recordInstallation('Vanilla/Components/Buttons/split-button', 'Vanilla HTML/CSS/JS');
  
  assert.strictEqual(isResourceInstalled('Vanilla/Components/Buttons/split-button'), true);
  assert.strictEqual(isResourceInstalled('React/Components/Buttons/solid-button'), false);
  teardown();
});

// Test: multiple installations are recorded
check('multiple installations are recorded', () => {
  setup();
  recordInstallation('Vanilla/Components/Buttons/split-button', 'Vanilla HTML/CSS/JS');
  recordInstallation('Tailwind/Components/Accordions/basic-accordion', 'Tailwind CSS');
  
  const config = readConfig();
  assert.strictEqual(config.resources.length, 2);
  teardown();
});

console.log('\nAll config tests passed\n');
