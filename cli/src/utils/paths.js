/**
 * DevSnips CLI - Path utilities for safe path handling
 */

const path = require('node:path');

/**
 * Normalize a user-provided path by:
 * - Removing trailing slashes
 * - Normalizing separators
 * - Preventing directory traversal
 * 
 * @param {string} inputPath - The raw path from user input
 * @returns {string|null} - Normalized path or null if invalid
 */
function normalizePath(inputPath) {
  if (!inputPath || typeof inputPath !== 'string') {
    return null;
  }

  // Trim whitespace
  let normalized = inputPath.trim();

  // Check for absolute paths (Unix or Windows)
  if (path.isAbsolute(normalized)) {
    return null;
  }

  // Check for directory traversal attempts
  if (normalized.includes('..')) {
    return null;
  }

  // Normalize path separators (convert backslashes to forward slashes)
  normalized = normalized.replace(/\\/g, '/');

  // Remove leading slashes
  normalized = normalized.replace(/^\/+/, '');

  // Remove trailing slashes
  normalized = normalized.replace(/\/+$/, '');

  // Check for empty result
  if (normalized.length === 0) {
    return null;
  }

  // Validate that path only contains safe characters
  // Allow: letters, numbers, hyphens, underscores, forward slashes, spaces
  if (!/^[\w\-/\s]+$/.test(normalized)) {
    return null;
  }

  return normalized;
}

/**
 * Validate that a path is repository-relative and safe
 * 
 * @param {string} repoPath - The repository-relative path
 * @returns {boolean} - True if valid
 */
function isValidRepoPath(repoPath) {
  if (!repoPath) return false;

  // Must start with a known technology
  const validTechnologies = ['Tailwind', 'React', 'Vanilla'];
  const firstSegment = repoPath.split('/')[0];
  
  if (!validTechnologies.includes(firstSegment)) {
    return false;
  }

  // Must not contain unsafe patterns
  if (repoPath.includes('..') || repoPath.includes('//')) {
    return false;
  }

  return true;
}

/**
 * Extract technology from a repository path
 * 
 * @param {string} repoPath - Repository-relative path
 * @returns {string|null} - Technology name or null
 */
function getTechnologyFromPath(repoPath) {
  const firstSegment = repoPath.split('/')[0];
  const techMap = {
    'Tailwind': 'tailwind',
    'React': 'react',
    'Vanilla': 'vanilla'
  };
  return techMap[firstSegment] || null;
}

/**
 * Build a safe destination path within the project
 * 
 * @param {string} projectRoot - The root of the user's project
 * @param {string} relativePath - Relative path within devsnips folder
 * @returns {string} - Absolute destination path
 */
function buildDestinationPath(projectRoot, relativePath) {
  const baseDir = path.join(projectRoot, 'devsnips');
  const safeRelative = relativePath.replace(/^\/+|\/+$/g, '');
  return path.join(baseDir, safeRelative);
}

/**
 * Ensure a path stays within a base directory (security check)
 * 
 * @param {string} basePath - Base directory
 * @param {string} targetPath - Target path to validate
 * @returns {boolean} - True if target is within base
 */
function isPathWithinBase(basePath, targetPath) {
  const resolvedBase = path.resolve(basePath);
  const resolvedTarget = path.resolve(targetPath);
  return resolvedTarget.startsWith(resolvedBase + path.sep) || resolvedTarget === resolvedBase;
}

module.exports = {
  normalizePath,
  isValidRepoPath,
  getTechnologyFromPath,
  buildDestinationPath,
  isPathWithinBase
};
