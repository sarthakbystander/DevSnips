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
const { initializeContext, updateContextAfterInstall } = require('../devsnips/context.js');

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

  // Step 7: Initialize/update DevSnips project context
  // This happens AFTER files are successfully written
  try {
    // Ensure context is initialized (creates config.json and AGENTS.md if missing)
    const initResult = initializeContext();
    
    // Record this installation in config.json
    const updateResult = updateContextAfterInstall(resolved.canonicalPath, resolved.technology);
    
    // Print context initialization messages
    console.log('');
    if (initResult.agentsCreated || initResult.configCreated) {
      console.log('  Initializing DevSnips project context... ✓');
      if (initResult.agentsCreated) {
        console.log('  Created devsnips/AGENTS.md');
      }
      if (initResult.configCreated) {
        console.log('  Created devsnips/config.json');
      }
    } else {
      console.log('  Updating DevSnips project context... ✓');
    }
  } catch (error) {
    // Context update failed but component was installed
    console.log('');
    console.error('  ⚠ Warning: Could not update DevSnips project context');
    console.error('');
    console.error('  ' + error.message);
    console.error('');
    console.error('  The component was installed successfully, but config.json could not be updated.');
    console.error('  Please check the devsnips/config.json file manually.');
    console.error('');
  }

  // Step 8: Report success
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
