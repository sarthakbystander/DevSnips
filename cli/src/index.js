#!/usr/bin/env node

/**
 * DevSnips CLI - Main entry point
 * 
 * Usage:
 *   npx devsnips add <path>
 *   npx devsnips --help
 */

const { parseArgs } = require('node:util');
const path = require('node:path');
const { runAddCommand } = require('./commands/add.js');
const { showHelp } = require('./utils/errors.js');

const args = process.argv.slice(2);

// Handle no arguments
if (args.length === 0) {
  showHelp();
  process.exit(1);
}

// Handle help flag
if (args.includes('--help') || args.includes('-h')) {
  showHelp();
  process.exit(0);
}

// Parse command
const command = args[0];

switch (command) {
  case 'add':
    const componentPath = args[1];
    if (!componentPath) {
      console.error('Error: Missing component path');
      console.error('');
      console.error('Usage:');
      console.error('  npx devsnips add <component-path>');
      console.error('');
      console.error('Example:');
      console.error('  npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel');
      process.exit(1);
    }
    runAddCommand(componentPath);
    break;
    
  default:
    console.error(`Unknown command: ${command}`);
    console.error('');
    console.error('Available commands:');
    console.error('  add    Install a component from DevSnips');
    console.error('');
    console.error('Run "npx devsnips --help" for more information.');
    process.exit(1);
}
