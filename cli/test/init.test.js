/**
 * Tests for DevSnips CLI init command
 *
 * Run with: node test/init.test.js
 */

const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { execSync } = require('node:child_process');

let testDir;
let originalCwd;
const cliPath = path.join(__dirname, '..', 'src', 'index.js');

function setup() {
  // Create isolated temp directory
  testDir = fs.mkdtempSync(path.join(os.tmpdir(), 'devsnips-init-test-'));
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

// Test: init creates devsnips directory
check('init creates devsnips directory', () => {
  setup();
  execSync(`node "${cliPath}" init`, { stdio: 'pipe' });
  
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  assert.ok(fs.existsSync(devsnipsDir));
  teardown();
});

// Test: init creates config.json
check('init creates config.json', () => {
  setup();
  execSync(`node "${cliPath}" init`, { stdio: 'pipe' });
  
  const configPath = path.join(process.cwd(), 'devsnips', 'config.json');
  assert.ok(fs.existsSync(configPath));
  
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  assert.strictEqual(config.version, 1);
  teardown();
});

// Test: init creates AGENTS.md
check('init creates AGENTS.md', () => {
  setup();
  execSync(`node "${cliPath}" init`, { stdio: 'pipe' });
  
  const agentsPath = path.join(process.cwd(), 'devsnips', 'AGENTS.md');
  assert.ok(fs.existsSync(agentsPath));
  
  const content = fs.readFileSync(agentsPath, 'utf8');
  assert.ok(content.includes('# DevSnips Agent Instructions'));
  teardown();
});

// Test: running init twice does not overwrite AGENTS.md
check('running init twice does not overwrite AGENTS.md', () => {
  setup();
  
  // First init
  execSync(`node "${cliPath}" init`, { stdio: 'pipe' });
  
  // Modify AGENTS.md
  const agentsPath = path.join(process.cwd(), 'devsnips', 'AGENTS.md');
  const customContent = '# Custom Agent Instructions\n\nMy custom content.';
  fs.writeFileSync(agentsPath, customContent, 'utf8');
  
  // Second init - should NOT overwrite
  execSync(`node "${cliPath}" init`, { stdio: 'pipe' });
  
  const content = fs.readFileSync(agentsPath, 'utf8');
  assert.strictEqual(content, customContent);
  teardown();
});

// Test: running init twice does not destroy config.json
check('running init twice does not destroy config.json', () => {
  setup();
  
  // First init
  execSync(`node "${cliPath}" init`, { stdio: 'pipe' });
  
  // Modify config.json
  const configPath = path.join(process.cwd(), 'devsnips', 'config.json');
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  config.project = { framework: 'react' };
  config.resources = [{ path: 'Test/Component', technology: 'Test', installedAt: new Date().toISOString() }];
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n', 'utf8');
  
  // Second init - should preserve config
  execSync(`node "${cliPath}" init`, { stdio: 'pipe' });
  
  const updatedConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  assert.deepStrictEqual(updatedConfig.project, { framework: 'react' });
  assert.strictEqual(updatedConfig.resources.length, 1);
  teardown();
});

// Test: help output mentions init command
check('help output mentions init command', () => {
  setup();
  const output = execSync(`node "${cliPath}" --help`, { encoding: 'utf8' });
  
  assert.ok(output.includes('init'));
  assert.ok(output.includes('Initialize the DevSnips project context'));
  teardown();
});

console.log('\nAll init tests passed\n');
