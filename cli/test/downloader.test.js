/**
 * Regression tests for the DevSnips CLI installer.
 *
 * Verifies that getSourceFiles() installs README.md and AGENTS.md when
 * present in the registry's resolved file list,and never installs
 * metadata.json or preview.html.
 *
 * Run with: node test/downloader.test.js
 */

const assert = require('node:assert');
const { getSourceFiles } = require('../src/install/downloader.js');

function check(name, available, expected) {
  const actual = getSourceFiles(available, 'Tailwind CSS');
  assert.deepStrictEqual(actual, expected, name);
}

// README.md and AGENTS.md are installable when present
check(
  'README.md is installable when present',
  ['code.html', 'README.md', 'metadata.json', 'preview.html'],
  ['code.html', 'README.md']
);
check(
  'AGENTS.md is installable when present',
  ['code.html', 'AGENTS.md', 'metadata.json', 'preview.html'],
  ['code.html', 'AGENTS.md']
);
check(
  'README.md and AGENTS.md are both installable',
  ['code.html', 'README.md', 'AGENTS.md', 'metadata.json', 'preview.html'],
  ['code.html', 'README.md', 'AGENTS.md']
);

// metadata.json and preview.html are always excluded
check(
  'metadata.json is excluded',
  ['code.html', 'metadata.json'],
  ['code.html']
);
check(
  'preview.html is excluded',
  ['code.html', 'preview.html'],
  ['code.html']
);
check(
  'metadata.json and preview.html are excluded together',
  ['metadata.json', 'preview.html'],
  []
);

// Existing source files remain installable
check(
  'source extensions remain installable',
  ['code.html', 'code.jsx', 'code.tsx', 'script.js', 'lib.ts', 'style.css'],
  ['code.html', 'code.jsx', 'code.tsx', 'script.js', 'lib.ts', 'style.css']
);

// Directories containing only README.md and/or AGENTS.md are handled
check(
  'README.md-only entry installs README',
  ['README.md'],
  ['README.md']
);
check(
  'AGENTS.md-only entry installs AGENTS',
  ['AGENTS.md'],
  ['AGENTS.md']
);
check(
  'README.md + AGENTS.md-only entry installs both',
  ['README.md', 'AGENTS.md'],
  ['README.md', 'AGENTS.md']
);
check(
  'entry with only skipped files installs nothing',
  ['metadata.json', 'preview.html'],
  []
);

// Nested template files are preserved,and files not present are never
// invented (this mirrors a real template registry file list).
check(
  'realistic template file list installs exactly the present files',
  [
    'pages/index.html',
    'pages/about.html',
    'pages/pricing.html',
    'README.md',
    'AGENTS.md',
    'metadata.json',
    'preview.html'
  ],
  ['pages/index.html', 'pages/about.html', 'pages/pricing.html', 'README.md', 'AGENTS.md']
);

console.log('All downloader tests passed');