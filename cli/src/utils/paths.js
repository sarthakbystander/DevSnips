/**
 * DevSnips CLI - Path utilities for safe path handling
 */

const path = require('node:path');

/**
 * Map registry technology names (and path prefixes) to clean directory slugs.
 */
const TECH_SLUG_MAP = {
  // From family.tech in snippets-index.json
  'Tailwind CSS': 'tailwind',
  'Vanilla HTML/CSS/JS': 'vanilla',
  'React': 'react',
  // From path first segment
  'Tailwind': 'tailwind',
  'Vanilla': 'vanilla',
  'React': 'react',
  // Already-normalized
  'tailwind': 'tailwind',
  'vanilla': 'vanilla',
  'react': 'react',
  'tailwind-css': 'tailwind',
  'tailwindcss': 'tailwind'
};

/**
 * Normalize a technology name or path prefix to a clean slug.
 *
 * @param {string} tech - Technology string from registry or path
 * @returns {string} - Clean slug (tailwind | react | vanilla)
 */
function toTechSlug(tech) {
  if (!tech || typeof tech !== 'string') return 'unknown';
  const trimmed = tech.trim();
  if (TECH_SLUG_MAP[trimmed]) return TECH_SLUG_MAP[trimmed];
  // Fallback: first word lowercased
  const first = trimmed.split(/[\s/]+/)[0].toLowerCase();
  return TECH_SLUG_MAP[first] || first.replace(/[^a-z0-9-]/g, '');
}

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

  // Remove trailing slashes (registry paths often end with /)
  normalized = normalized.replace(/\/+$/, '');

  // Collapse multiple consecutive slashes
  normalized = normalized.replace(/\/+/g, '/');

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
 * Validate that a path is repository-relative and safe.
 * First segment is matched case-insensitively against known technologies.
 *
 * @param {string} repoPath - The repository-relative path
 * @returns {boolean} - True if valid
 */
function isValidRepoPath(repoPath) {
  if (!repoPath) return false;

  // Must start with a known technology (case-insensitive)
  const validTechnologies = ['tailwind', 'react', 'vanilla'];
  const firstSegment = repoPath.split('/')[0].toLowerCase();

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
 * Extract technology slug from a repository path.
 *
 * @param {string} repoPath - Repository-relative path
 * @returns {string|null} - Technology slug or null
 */
function getTechnologyFromPath(repoPath) {
  if (!repoPath) return null;
  const firstSegment = repoPath.split('/')[0];
  return toTechSlug(firstSegment);
}

/**
 * Build a safe destination path within the project.
 *
 * @param {string} projectRoot - The root of the user's project
 * @param {string} relativePath - Relative path within devsnips folder
 * @returns {string} - Absolute destination path
 */
function buildDestinationPath(projectRoot, relativePath) {
  const baseDir = path.join(projectRoot, 'devsnips');
  const safeRelative = relativePath.replace(/^\/+|\/+$/g, '').replace(/\/+/g, '/');
  return path.join(baseDir, safeRelative);
}

/**
 * Ensure a path stays within a base directory (security check).
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

/**
 * Strip trailing slash and normalize separators for comparison/matching.
 *
 * @param {string} p - Path
 * @returns {string}
 */
function stripTrailingSlash(p) {
  if (!p || typeof p !== 'string') return '';
  return p.replace(/\\/g, '/').replace(/\/+$/, '');
}

module.exports = {
  normalizePath,
  isValidRepoPath,
  getTechnologyFromPath,
  buildDestinationPath,
  isPathWithinBase,
  toTechSlug,
  stripTrailingSlash,
  TECH_SLUG_MAP
};
