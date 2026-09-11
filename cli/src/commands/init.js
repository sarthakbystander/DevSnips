/**
 * DevSnips CLI - Init command implementation
 *
 * Initializes the DevSnips project context by creating:
 * - ./devsnips/ directory
 * - ./devsnips/config.json (if missing)
 * - ./devsnips/AGENTS.md (if missing)
 */

const { initializeContext, isContextInitialized } = require('../devsnips/context.js');

/**
 * Execute the init command
 */
function runInitCommand() {
  console.log('DevSnips');
  console.log('');
  
  // Check if already initialized
  if (isContextInitialized()) {
    console.log('  DevSnips project context already initialized.');
    console.log('');
    console.log('  devsnips/AGENTS.md exists');
    console.log('  devsnips/config.json exists');
    console.log('');
    console.log('✓ No changes made (existing files preserved)');
    console.log('');
    process.exit(0);
    return;
  }
  
  console.log('  Initializing DevSnips project context... ');
  
  try {
    const result = initializeContext();
    
    console.log('  ✓');
    console.log('');
    
    if (result.agentsCreated) {
      console.log('  Created devsnips/AGENTS.md');
    } else {
      console.log('  devsnips/AGENTS.md already exists');
    }
    
    if (result.configCreated) {
      console.log('  Created devsnips/config.json');
    } else {
      console.log('  devsnips/config.json already exists');
    }
    
    console.log('');
    console.log('✓ DevSnips project initialized successfully');
    console.log('');
    
    process.exit(0);
  } catch (error) {
    console.log('  ✗');
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
