/**
 * Tests for DevSnips CLI path utilities
 *
 * Run with: node test/paths.test.js
 */

const assert = require('node:assert');
const path = require('node:path');

const {
  normalizePath,
  isValidRepoPath,
  getTechnologyFromPath,
  buildDestinationPath,
  isPathWithinBase,
  toTechSlug,
  stripTrailingSlash
} = require('../src/utils/paths.js');

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

// --- normalizePath ---

check('normalizePath accepts a valid repository path', () => {
  assert.strictEqual(
    normalizePath('Tailwind/Sections/AI-Product/agent-workflow/vercel'),
    'Tailwind/Sections/AI-Product/agent-workflow/vercel'
  );
});

check('normalizePath strips trailing slashes and collapses separators', () => {
  assert.strictEqual(normalizePath('React/Components/Buttons/solid-button//'), 'React/Components/Buttons/solid-button');
  assert.strictEqual(normalizePath('Vanilla\\Components\\Tooltips\\tooltip'), 'Vanilla/Components/Tooltips/tooltip');
});

check('normalizePath rejects empty, non-string, and whitespace-only input', () => {
  assert.strictEqual(normalizePath(''), null);
  assert.strictEqual(normalizePath(null), null);
  assert.strictEqual(normalizePath(undefined), null);
  assert.strictEqual(normalizePath(123), null);
  assert.strictEqual(normalizePath('   '), null);
});

check('normalizePath rejects absolute paths', () => {
  assert.strictEqual(normalizePath('/etc/passwd'), null);
  assert.strictEqual(normalizePath('C:\\projects\\evil'), null);
});

check('normalizePath rejects directory traversal', () => {
  assert.strictEqual(normalizePath('Tailwind/../secrets'), null);
  assert.strictEqual(normalizePath('..'), null);
});

check('normalizePath rejects unsafe characters', () => {
  assert.strictEqual(normalizePath('Tailwind/Components/<script>'), null);
  assert.strictEqual(normalizePath('Tailwind/Components/x?y'), null);
});

// --- isValidRepoPath ---

check('isValidRepoPath accepts paths starting with a known technology', () => {
  assert.strictEqual(isValidRepoPath('Tailwind/Sections/Faq/accordion'), true);
  assert.strictEqual(isValidRepoPath('react/components/button'), true);
  assert.strictEqual(isValidRepoPath('VANILLA/Components/Tooltips/tooltip'), true);
});

check('isValidRepoPath rejects unknown technologies and unsafe patterns', () => {
  assert.strictEqual(isValidRepoPath('Angular/Components/button'), false);
  assert.strictEqual(isValidRepoPath('Tailwind/../secret'), false);
  assert.strictEqual(isValidRepoPath('Tailwind//double'), false);
  assert.strictEqual(isValidRepoPath(''), false);
  assert.strictEqual(isValidRepoPath(null), false);
});

// --- toTechSlug ---

check('toTechSlug maps registry technology names and path prefixes', () => {
  assert.strictEqual(toTechSlug('Tailwind CSS'), 'tailwind');
  assert.strictEqual(toTechSlug('Vanilla HTML/CSS/JS'), 'vanilla');
  assert.strictEqual(toTechSlug('React'), 'react');
  assert.strictEqual(toTechSlug('tailwindcss'), 'tailwind');
});

check('toTechSlug falls back to first word, lowercased and cleaned', () => {
  assert.strictEqual(toTechSlug('Svelte Kit'), 'svelte');
  assert.strictEqual(toTechSlug(null), 'unknown');
  assert.strictEqual(toTechSlug(''), 'unknown');
});

// --- getTechnologyFromPath ---

check('getTechnologyFromPath extracts the slug from the first segment', () => {
  assert.strictEqual(getTechnologyFromPath('Tailwind/Sections/Faq/accordion'), 'tailwind');
  assert.strictEqual(getTechnologyFromPath('react/components/button'), 'react');
  assert.strictEqual(getTechnologyFromPath(null), null);
});

// --- buildDestinationPath ---

check('buildDestinationPath joins project root with devsnips base', () => {
  const root = path.resolve('my-project');
  const dest = buildDestinationPath(root, 'tailwind/sections/faq/accordion');
  assert.strictEqual(dest, path.join(root, 'devsnips', 'tailwind', 'sections', 'faq', 'accordion'));
});

check('buildDestinationPath cleans leading/trailing/duplicate slashes', () => {
  const root = path.resolve('my-project');
  const dest = buildDestinationPath(root, '/tailwind//sections/');
  assert.strictEqual(dest, path.join(root, 'devsnips', 'tailwind', 'sections'));
});

// --- isPathWithinBase (security) ---

check('isPathWithinBase accepts paths inside the base and the base itself', () => {
  const base = path.resolve('proj', 'devsnips');
  assert.strictEqual(isPathWithinBase(base, path.join(base, 'tailwind', 'x.html')), true);
  assert.strictEqual(isPathWithinBase(base, base), true);
});

check('isPathWithinBase rejects paths outside the base', () => {
  const base = path.resolve('proj', 'devsnips');
  assert.strictEqual(isPathWithinBase(base, path.resolve('proj', 'other', 'x.html')), false);
  assert.strictEqual(isPathWithinBase(base, path.resolve('x.html')), false);
});

check('isPathWithinBase rejects sibling directories sharing a name prefix', () => {
  // "devsnips-evil" starts with "devsnips" but must not pass the check
  const base = path.resolve('proj', 'devsnips');
  assert.strictEqual(isPathWithinBase(base, path.resolve('proj', 'devsnips-evil', 'x.html')), false);
});

check('isPathWithinBase rejects traversal targets after normalization', () => {
  const base = path.resolve('proj', 'devsnips');
  assert.strictEqual(
    isPathWithinBase(base, path.resolve(base, '..', 'escaped.html')),
    false
  );
});

// --- stripTrailingSlash ---

check('stripTrailingSlash normalizes separators and trailing slashes', () => {
  assert.strictEqual(stripTrailingSlash('Tailwind/Sections/'), 'Tailwind/Sections');
  assert.strictEqual(stripTrailingSlash('Vanilla\\Components\\'), 'Vanilla/Components');
  assert.strictEqual(stripTrailingSlash(''), '');
  assert.strictEqual(stripTrailingSlash(null), '');
});

console.log('paths.test.js: all checks passed');
