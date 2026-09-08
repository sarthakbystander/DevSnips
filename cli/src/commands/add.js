/**
 * DevSnips CLI - Add command implementation
 *
 * Main entry point for: npx devsnips add <path>
 */

const { normalizePath, isValidRepoPath } = require('../utils/paths.js');
const { exitWithError } = require('../utils/errors.js');
const { fetchRegistry, resolveComponent, findSimilarPaths } = require('../registry/resolver.js');
const { downloadFile, getSourceFiles, buildRepoFilePath } = require('../install/downloader.js');
const { calculateDestination, getDestinationFilePath, writeFile } = require('../install/writer.js');

/**
 * Execute the add command
 *
 * @param {string} inputPath - User-provided component path
 */
async function runAddCommand(inputPath) {
  // Step 1: Normalize and validate input path
  const normalizedPath = normalizePath(inputPath);

  if (!normalizedPath) {
    exitWithError(
      'Invalid component path',
      [
        `Input: ${inputPath}`,
        '',
        'The path must be a valid repository-relative path.',
        'Example: Tailwind/Sections/AI-Product/agent-workflow/vercel'
      ]
    );
  }

  if (!isValidRepoPath(normalizedPath)) {
    exitWithError(
      'Invalid repository path',
      [
        `Path: ${normalizedPath}`,
        '',
        'The path must start with a valid technology:',
        '  - Tailwind',
        '  - React',
        '  - Vanilla'
      ]
    );
  }

  // Step 2: Fetch registry
  console.log('DevSnips');
  console.log('');
  process.stdout.write('  Resolving component... ');

  const registry = await fetchRegistry();

  // Step 3: Resolve component
  const resolved = resolveComponent(normalizedPath, registry);

  if (!resolved) {
    // Try to find similar paths for helpful error message
    const similar = findSimilarPaths(normalizedPath, registry);

    let details = [
      `Path: ${normalizedPath}`,
      '',
      'This component was not found in the DevSnips registry.'
    ];

    if (similar.length > 0) {
      details.push('');
      details.push('Did you mean one of these?');
      similar.forEach(s => details.push(`  - ${s}`));
    }

    details.push('');
    details.push('Check the path or browse available components at:');
    details.push('  https://github.com/sarthakbystander/DevSnips');

    exitWithError('Component not found', details);
  }

  console.log('✓');

  // Step 4: Determine source files to install
  const sourceFiles = getSourceFiles(resolved.files, resolved.technology);

  if (sourceFiles.length === 0) {
    exitWithError(
      'No source files found',
      [
        `Component: ${resolved.canonicalPath}`,
        '',
        'This component does not have any installable source files.',
        'It may only contain metadata or preview files.'
      ]
    );
  }

  // Step 5: Download all source files
  const downloadedFiles = new Map(); // filename -> content

  for (const file of sourceFiles) {
    const repoFilePath = buildRepoFilePath(resolved.canonicalPath, file);
    process.stdout.write(`  Downloading ${file}... `);

    try {
      const content = await downloadFile(repoFilePath);

      // Validate content is not empty
      if (!content || content.trim().length === 0) {
        throw new Error('Empty file');
      }

      downloadedFiles.set(file, content);
      console.log('✓');
    } catch (error) {
      console.log('✗');
      exitWithError(
        'Download failed',
        [
          `File: ${file}`,
          `Component: ${resolved.canonicalPath}`,
          `Error: ${error.message}`
        ]
      );
    }
  }

  // Step 6: Calculate destination and write files
  const destDir = calculateDestination(resolved.canonicalPath, resolved.technology);

  const writtenFiles = [];

  for (const [filename, content] of downloadedFiles) {
    const destPath = getDestinationFilePath(destDir, filename);

    try {
      writeFile(destPath, content, false);
      writtenFiles.push(filename);
    } catch (error) {
      // writeFile already exits on error
    }
  }

  // Step 7: Report success
  console.log('');
  console.log('✓ Component installed successfully');
  console.log('');
  console.log(`  Location: ${destDir}`);
  console.log(`  Files:`);
  writtenFiles.forEach(f => console.log(`    - ${f}`));
  console.log('');

  // Exit with success
  process.exit(0);
}

module.exports = {
  runAddCommand
};
