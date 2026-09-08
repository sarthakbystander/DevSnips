/**
 * DevSnips CLI - File writer
 * 
 * Safely writes downloaded files to the destination directory.
 */

const fs = require('node:fs');
const path = require('node:path');
const { exitWithFilesystemError } = require('../utils/errors.js');
const { isPathWithinBase, buildDestinationPath } = require('../utils/paths.js');

/**
 * Ensure a directory exists, creating it if necessary
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
 * Check if a file already exists at the destination
 * 
 * @param {string} filePath - Full file path
 * @returns {boolean} - True if file exists
 */
function fileExists(filePath) {
  return fs.existsSync(filePath);
}

/**
 * Write a file safely (fails if file already exists)
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
      'File already exists. Remove it first or use --force (not yet implemented).',
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
 * Calculate the destination directory for a component
 * 
 * V1 destination strategy:
 * ./devsnips/<technology-slug>/<family-slug>/<variant-slug>/
 * 
 * Example:
 *   Input: Tailwind/Sections/AI-Product/agent-workflow/vercel
 *   Output: ./devsnips/tailwind/ai-product/agent-workflow/vercel/
 * 
 * @param {string} canonicalPath - Canonical repository path
 * @param {string} technology - Technology name from registry
 * @returns {string} - Destination directory path
 */
function calculateDestination(canonicalPath, technology) {
  const projectRoot = process.cwd();
  
  // Normalize technology to lowercase for directory naming
  const techSlug = technology.toLowerCase().replace(/\s+/g, '-');
  
  // Build destination relative to project root
  // The canonical path is like: Tailwind/Sections/AI-Product/agent-workflow/vercel
  // We want: devsnips/tailwind/sections/ai-product/agent-workflow/vercel
  const normalizedPath = canonicalPath.replace(/\/+$/, '');
  
  return buildDestinationPath(projectRoot, `${techSlug}/${normalizedPath}`);
}

/**
 * Get the destination file path for a source file
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
