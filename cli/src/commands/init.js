/**
 * DevSnips CLI - Init command implementation
 *
 * Initializes the DevSnips project context by creating:
 * - ./devsnips/ directory
 * - ./devsnips/config.json (if missing)
 * - ./devsnips/AGENTS.md (if missing)
 *
 * Existing files are always preserved.
 */

const { initializeContext, isContextInitialized } = require('../devsnips/context.js');

/**
 * Execute the init command.
 */
function runInitCommand() {
  console.log('DevSnips');
  console.log('');

  // Both context files already exist - nothing to create
  if (isContextInitialized()) {
    console.log('  DevSnips project context already initialized.');
    console.log('');
    process.exit(0);
    return;
  }

  process.stdout.write('  Initializing DevSnips project context... ');

  try {
    const result = initializeContext();
    console.log('✓');

    if (result.agentsCreated) {
      console.log('  Created devsnips/AGENTS.md');
    }
    if (result.configCreated) {
      console.log('  Created devsnips/config.json');
    }

    console.log('');
    console.log('✓ DevSnips project initialized successfully');
    console.log('');
    process.exit(0);
  } catch (error) {
    console.log('✗');
    console.log('');
    console.error('✗ Initialization failed');
    console.error('');
    console.error('  ' + error.message);
    console.error('');
    process.exit(1);
  }
}

module.exports = {
  runInitCommand
};
