/**
 * Tests for DevSnips CLI registry resolver (pure functions, no network)
 *
 * Run with: node test/resolver.test.js
 */

const assert = require('node:assert');

const { resolveComponent, findSimilarPaths } = require('../src/registry/resolver.js');

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

// Minimal registry fixture shaped like snippets-index.json
const REGISTRY = {
  families: [
    {
      name: 'Buttons',
      tech: 'React',
      type: 'component',
      category: 'Components',
      variants: [
        {
          path: 'React/Components/Buttons/solid-button',
          type: 'component',
          files: ['code.tsx']
        },
        {
          path: 'React/Components/Buttons/outline-button',
          type: 'component',
          files: ['code.tsx']
        }
      ]
    },
    {
      name: 'FAQ',
      tech: 'Tailwind CSS',
      type: 'section',
      category: 'Sections',
      variants: [
        {
          path: 'Tailwind/Sections/FAQ/accordion',
          type: 'section',
          files: ['code.html', 'preview.html']
        }
      ]
    },
    {
      name: 'Navigation',
      tech: 'Vanilla HTML/CSS/JS',
      type: 'component',
      category: 'Components',
      variants: [
        { path: 'Vanilla/Components/Navigation/hamburger-menu', files: ['code.html'] },
        { path: 'Vanilla/Components/Navigation/top-navigation', files: ['code.html'] },
        { path: 'Vanilla/Components/Navigation/side-navigation', files: ['code.html'] },
        { path: 'Vanilla/Components/Navigation/mega-menu', files: ['code.html'] },
        { path: 'Vanilla/Components/Navigation/breadcrumb-nav', files: ['code.html'] },
        { path: 'Vanilla/Components/Navigation/pagination-component', files: ['code.html'] }
      ]
    },
    {
      // Family without variants must be skipped, not crash
      name: 'Empty',
      tech: 'React',
      variants: null
    }
  ]
};

// --- resolveComponent ---

check('resolveComponent returns null for unknown paths', () => {
  assert.strictEqual(resolveComponent('React/Components/Buttons/nope', REGISTRY), null);
  assert.strictEqual(resolveComponent('Angular/Components/button', REGISTRY), null);
});

check('resolveComponent matches exactly', () => {
  const resolved = resolveComponent('React/Components/Buttons/solid-button', REGISTRY);
  assert.strictEqual(resolved.variant.path, 'React/Components/Buttons/solid-button');
  assert.strictEqual(resolved.technology, 'React');
  assert.strictEqual(resolved.type, 'component');
  assert.strictEqual(resolved.family.name, 'Buttons');
  assert.deepStrictEqual(resolved.files, ['code.tsx']);
  assert.strictEqual(resolved.canonicalPath, 'React/Components/Buttons/solid-button');
});

check('resolveComponent matches case-insensitively', () => {
  const resolved = resolveComponent('react/components/buttons/solid-button', REGISTRY);
  assert.strictEqual(resolved.variant.path, 'React/Components/Buttons/solid-button');
});

check('resolveComponent ignores trailing slashes', () => {
  const resolved = resolveComponent('Tailwind/Sections/FAQ/accordion/', REGISTRY);
  assert.strictEqual(resolved.technology, 'Tailwind CSS');
  assert.strictEqual(resolved.canonicalPath, 'Tailwind/Sections/FAQ/accordion');
});

check('resolveComponent skips families without variants', () => {
  assert.strictEqual(resolveComponent('Empty', REGISTRY), null);
});

// --- findSimilarPaths ---

check('findSimilarPaths returns prefix matches', () => {
  const similar = findSimilarPaths('React/Components/Buttons', REGISTRY);
  assert.deepStrictEqual(similar, [
    'React/Components/Buttons/solid-button',
    'React/Components/Buttons/outline-button'
  ]);
});

check('findSimilarPaths matches when the input extends a variant path', () => {
  const similar = findSimilarPaths('Vanilla/Components/Navigation/hamburger-menu/extra', REGISTRY);
  assert.deepStrictEqual(similar, ['Vanilla/Components/Navigation/hamburger-menu']);
});

check('findSimilarPaths is case-insensitive and slash-insensitive', () => {
  const similar = findSimilarPaths('tailwind/sections/faq/accordion/', REGISTRY);
  assert.deepStrictEqual(similar, ['Tailwind/Sections/FAQ/accordion']);
});

check('findSimilarPaths returns at most 5 results', () => {
  const similar = findSimilarPaths('Vanilla/Components/Navigation', REGISTRY);
  assert.strictEqual(similar.length, 5);
});

check('findSimilarPaths returns empty list when nothing matches', () => {
  assert.deepStrictEqual(findSimilarPaths('Nothing/At/All', REGISTRY), []);
});

console.log('resolver.test.js: all checks passed');
