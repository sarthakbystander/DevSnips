/**
 * Tests for DevSnips CLI AGENTS.md management
 *
 * Run with: node test/agents.test.js
 */

const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const {
  getAgentsPath,
  getDefaultAgentsContent,
  ensureAgents,
  agentsExists,
  readAgents
} = require('../src/devsnips/agents.js');

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

// Test: getAgentsPath returns correct path
check('getAgentsPath returns correct path', () => {
  const agentsPath = getAgentsPath();
  const expected = path.join(process.cwd(), 'devsnips', 'AGENTS.md');
  assert.strictEqual(agentsPath, expected);
});

// Test: getDefaultAgentsContent returns non-empty string
check('getDefaultAgentsContent returns non-empty string', () => {
  const content = getDefaultAgentsContent();
  assert.ok(typeof content === 'string');
  assert.ok(content.length > 0);
  assert.ok(content.includes('# DevSnips Agent Instructions'));
});

// Test: ensureAgents creates file when missing
check('ensureAgents creates file when missing', () => {
  setup();
  const result = ensureAgents();
  
  assert.strictEqual(result.created, true);
  assert.ok(fs.existsSync(getAgentsPath()));
  
  const content = readAgents();
  assert.ok(content.includes('# DevSnips Agent Instructions'));
  teardown();
});

// Test: ensureAgents does NOT overwrite existing file
check('ensureAgents does NOT overwrite existing file', () => {
  setup();
  
  // Create custom AGENTS.md
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  fs.mkdirSync(devsnipsDir, { recursive: true });
  const agentsPath = path.join(devsnipsDir, 'AGENTS.md');
  const customContent = '# Custom Agent Instructions\n\nMy custom content here.';
  fs.writeFileSync(agentsPath, customContent, 'utf8');
  
  // Call ensureAgents - should NOT overwrite
  const result = ensureAgents();
  
  assert.strictEqual(result.created, false);
  
  const content = fs.readFileSync(agentsPath, 'utf8');
  assert.strictEqual(content, customContent);
  teardown();
});

// Test: agentsExists returns correct values
check('agentsExists returns correct values', () => {
  setup();
  
  assert.strictEqual(agentsExists(), false);
  
  ensureAgents();
  
  assert.strictEqual(agentsExists(), true);
  teardown();
});

// Test: readAgents returns null when file does not exist
check('readAgents returns null when file does not exist', () => {
  setup();
  const content = readAgents();
  assert.strictEqual(content, null);
  teardown();
});

// Test: readAgents returns content when file exists
check('readAgents returns content when file exists', () => {
  setup();
  ensureAgents();
  const content = readAgents();
  assert.ok(typeof content === 'string');
  assert.ok(content.includes('# DevSnips Agent Instructions'));
  teardown();
});

// Test: ensureAgents creates devsnips directory if missing
check('ensureAgents creates devsnips directory if missing', () => {
  setup();
  ensureAgents();
  
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  assert.ok(fs.existsSync(devsnipsDir));
  teardown();
});

console.log('\nAll agents tests passed\n');
