/**
 * DevSnips CLI - Error handling and help utilities
 */

const PACKAGE_VERSION = require('../../package.json').version;

function showHelp() {
  console.log(`
DevSnips CLI - Install UI components from the DevSnips library

Usage:
  npx devsnips <command> [options]

Commands:
  add <path>    Install a component/resource from DevSnips
  init          Initialize the DevSnips project context

Examples:
  npx devsnips add Tailwind/Sections/AI-Product/agent-workflow/vercel
  npx devsnips add React/Components/Buttons/solid-button
  npx devsnips add Vanilla/Components/Buttons/split-button
  npx devsnips init

Path format:
  The path must match the DevSnips repository structure:
  <Technology>/<Category>/<Family>/<variant>/[style]

  Examples:
    Tailwind/Components/Accordions/basic-accordion
    Tailwind/Sections/AI-Product/agent-workflow/vercel
    React/Components/Buttons/solid-button
    Vanilla/Components/Buttons/split-button

Destination:
  Components are installed under:
    ./devsnips/<tech>/<category>/<family>/<variant>/

  where <tech> is one of: tailwind, react, vanilla
  (the leading technology segment is stripped and normalized so it
  appears only once; remaining path segments are lowercased).

  Example:
    Input:  Tailwind/Sections/AI-Product/agent-workflow/vercel
    Output: ./devsnips/tailwind/sections/ai-product/agent-workflow/vercel/

Project Context:
  DevSnips maintains project context in:
    ./devsnips/config.json     - Machine-readable project state
    ./devsnips/AGENTS.md       - Instructions for AI coding agents

  The \`init\` command creates this context manually, or it is
  initialized automatically the first time you run \`add\`.

  Once created, AGENTS.md is never overwritten automatically.
  You may edit it to add project-specific instructions.

Options:
  --help, -h    Show this help message
  --version, -v  Show the installed version

For more information, visit: https://github.com/sarthakbystander/DevSnips
`);
}

function exitWithError(message, details = null) {
  console.error('');
  console.error('✗ ' + message);
  console.error('');
  if (details) {
    if (Array.isArray(details)) {
      details.forEach(line => console.error('  ' + line));
    } else {
      console.error('  ' + details);
    }
    console.error('');
  }
  process.exit(1);
}

function exitWithNetworkError(message) {
  console.error('');
  console.error('✗ Network error');
  console.error('');
  console.error('  ' + message);
  console.error('');
  console.error('  Check your internet connection and try again.');
  console.error('');
  process.exit(1);
}

function exitWithFilesystemError(message, filePath = null) {
  console.error('');
  console.error('✗ Filesystem error');
  console.error('');
  if (filePath) {
    console.error('  Path: ' + filePath);
  }
  console.error('  ' + message);
  console.error('');
  process.exit(1);
}

function printVersion() {
  console.log(PACKAGE_VERSION);
}

module.exports = {
  showHelp,
  exitWithError,
  exitWithNetworkError,
  exitWithFilesystemError,
  printVersion
};
