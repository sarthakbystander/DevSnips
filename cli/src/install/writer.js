/**
 * DevSnips CLI - File writer
 *
 * Safely writes downloaded files to the destination directory.
 */

const fs = require('node:fs');
const path = require('node:path');
const { exitWithFilesystemError } = require('../utils/errors.js');
const {
  isPathWithinBase,
  buildDestinationPath,
  toTechSlug,
  stripTrailingSlash
} = require('../utils/paths.js');

/**
 * Ensure a directory exists, creating it if necessary.
 *
 * @param {string} dirPath - Directory path to ensure exists
 */
function ensureDirectory(dirPath) {
  try {
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }
  } catch (error) {
    exitWithFilesystemError(`Failed to create directory: ${error.message}`, dirPath);
  }
}

/**
 * Check if a file already exists at the destination.
 *
 * @param {string} filePath - Full file path
 * @returns {boolean} - True if file exists
 */
function fileExists(filePath) {
  return fs.existsSync(filePath);
}

/**
 * Write a file safely (fails if file already exists unless allowOverwrite).
 *
 * @param {string} filePath - Destination file path
 * @param {string} content - File content
 * @param {boolean} allowOverwrite - Whether to overwrite existing files
 * @returns {boolean} - True if written successfully
 */
function writeFile(filePath, content, allowOverwrite = false) {
  // Security check: ensure path is within expected base
  const projectRoot = process.cwd();
  const devsnipsBase = path.join(projectRoot, 'devsnips');

  if (!isPathWithinBase(devsnipsBase, filePath)) {
    exitWithFilesystemError(
      'Security violation: attempted write outside devsnips directory',
      filePath
    );
  }

  // Check for existing file
  if (fileExists(filePath) && !allowOverwrite) {
    exitWithFilesystemError(
      'File already exists. Remove it first or re-run with --force once that flag is available.',
      filePath
    );
  }

  try {
    // Ensure parent directory exists
    const parentDir = path.dirname(filePath);
    ensureDirectory(parentDir);

    // Write the file
    fs.writeFileSync(filePath, content, 'utf8');
    return true;
  } catch (error) {
    exitWithFilesystemError(`Failed to write file: ${error.message}`, filePath);
  }
}

/**
 * Calculate the destination directory for a component.
 *
 * Destination strategy (clean, no duplication):
 *   ./devsnips/<tech-slug>/<rest-of-path-lowercased>/
 *
 * Example:
 *   Input canonical: Tailwind/Sections/AI-Product/agent-workflow/vercel
 *   tech:            Tailwind CSS
 *   Output:          ./devsnips/tailwind/sections/ai-product/agent-workflow/vercel
 *
 * The leading technology segment of the canonical path is stripped so the
 * tech slug appears only once. Remaining segments are lowercased for a
 * consistent on-disk layout.
 *
 * @param {string} canonicalPath - Canonical repository path (may have trailing /)
 * @param {string} technology - Technology name from registry (e.g. "Tailwind CSS")
 * @returns {string} - Destination directory path (absolute)
 */
function calculateDestination(canonicalPath, technology) {
  const projectRoot = process.cwd();
  const techSlug = toTechSlug(technology);

  // Normalize: strip trailing slash, normalize separators
  let relative = stripTrailingSlash(canonicalPath);

  // Drop the leading technology segment if present (case-insensitive)
  // e.g. "Tailwind/Sections/..." → "Sections/..."
  const segments = relative.split('/').filter(Boolean);
  if (segments.length > 0) {
    const firstLower = segments[0].toLowerCase();
    if (['tailwind', 'react', 'vanilla'].includes(firstLower)) {
      segments.shift();
    }
  }

  // Lowercase remaining segments for consistent destination layout
  const rest = segments.map(s => s.toLowerCase()).join('/');

  const destRelative = rest ? `${techSlug}/${rest}` : techSlug;
  return buildDestinationPath(projectRoot, destRelative);
}

/**
 * Get the destination file path for a source file.
 *
 * @param {string} destDir - Destination directory
 * @param {string} filename - Source filename
 * @returns {string} - Full destination file path
 */
function getDestinationFilePath(destDir, filename) {
  return path.join(destDir, filename);
}

module.exports = {
  ensureDirectory,
  fileExists,
  writeFile,
  calculateDestination,
  getDestinationFilePath
};
