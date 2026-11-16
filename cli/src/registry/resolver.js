/**
 * DevSnips CLI - Registry resolver
 *
 * Fetches and parses the snippets-index.json from the DevSnips repository
 * to resolve component paths to their canonical locations.
 */

const { exitWithNetworkError } = require('../utils/errors.js');
const { stripTrailingSlash } = require('../utils/paths.js');
const { httpGetText } = require('../utils/http.js');

const DEFAULT_REGISTRY_URL = 'https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json';
const DEFAULT_RAW_BASE = 'https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/';

let cachedRegistry = null;

/**
 * Registry index URL. Overridable for tests, mirrors, and offline use via
 * the DEVSNIPS_REGISTRY_URL environment variable.
 *
 * @returns {string} - The registry URL
 */
function getRegistryUrl() {
  return process.env.DEVSNIPS_REGISTRY_URL || DEFAULT_REGISTRY_URL;
}

/**
 * Base URL for raw file downloads. Overridable for tests, mirrors, and
 * offline use via the DEVSNIPS_RAW_BASE environment variable.
 *
 * @returns {string} - The raw base URL with a trailing slash
 */
function getRawBase() {
  const base = process.env.DEVSNIPS_RAW_BASE;
  if (base) {
    return stripTrailingSlash(base) + '/';
  }
  return DEFAULT_RAW_BASE;
}

/**
 * Fetch JSON from a URL.
 *
 * @param {string} url - The URL to fetch
 * @returns {Promise<object>} - Parsed JSON response
 */
async function fetchJSON(url) {
  const data = await httpGetText(url);
  try {
    return JSON.parse(data);
  } catch (e) {
    throw new Error('Invalid JSON response');
  }
}

/**
 * Fetch the registry from GitHub.
 *
 * @returns {Promise<object>} - The registry object
 */
async function fetchRegistry() {
  if (cachedRegistry) {
    return cachedRegistry;
  }

  try {
    const registry = await fetchJSON(getRegistryUrl());

    // Validate registry structure
    if (!registry || typeof registry !== 'object') {
      throw new Error('Invalid registry format');
    }

    if (!Array.isArray(registry.families)) {
      throw new Error('Registry missing families array');
    }

    cachedRegistry = registry;
    return registry;
  } catch (error) {
    if (error.code === 'ENOTFOUND' || error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT') {
      exitWithNetworkError('Could not reach DevSnips registry');
    }
    exitWithNetworkError(`Failed to fetch registry: ${error.message}`);
  }
}

/**
 * Normalize a path for comparison (strip trailing slashes, lowercase).
 *
 * @param {string} p - Path to normalize
 * @returns {string} - Normalized path
 */
function normalizeForMatch(p) {
  return stripTrailingSlash(p).toLowerCase();
}

/**
 * Resolve a user-provided path to a canonical component in the registry.
 *
 * @param {string} inputPath - User-provided path (already normalized, no trailing slash)
 * @param {object} registry - The registry object
 * @returns {object|null} - Resolved component info or null
 */
function resolveComponent(inputPath, registry) {
  const normalizedInput = normalizeForMatch(inputPath);

  // Search through all families and variants
  for (const family of registry.families) {
    if (!family.variants || !Array.isArray(family.variants)) {
      continue;
    }

    for (const variant of family.variants) {
      const variantPath = variant.path;
      if (!variantPath) continue;

      const normalizedVariant = normalizeForMatch(variantPath);

      // Exact match (case-insensitive, trailing-slash insensitive)
      if (normalizedVariant === normalizedInput) {
        return {
          family: family,
          variant: variant,
          canonicalPath: stripTrailingSlash(variantPath),
          technology: family.tech,
          type: variant.type || family.type,
          category: family.category,
          files: variant.files || []
        };
      }
    }
  }

  return null;
}

/**
 * Get the list of available variants for a partial path (for helpful error messages).
 *
 * @param {string} partialPath - Partial path provided by user
 * @param {object} registry - The registry object
 * @returns {string[]} - List of matching variant paths
 */
function findSimilarPaths(partialPath, registry) {
  const normalizedInput = normalizeForMatch(partialPath);
  const similar = [];

  for (const family of registry.families) {
    if (!family.variants || !Array.isArray(family.variants)) {
      continue;
    }

    for (const variant of family.variants) {
      const variantPath = variant.path;
      if (!variantPath) continue;

      const normalizedVariant = normalizeForMatch(variantPath);

      // Check if the variant path starts with the input (partial match)
      if (normalizedVariant.startsWith(normalizedInput) || normalizedInput.startsWith(normalizedVariant)) {
        similar.push(stripTrailingSlash(variantPath));
      }
    }
  }

  // Prefer shorter / closer matches, limit to 5
  similar.sort((a, b) => a.length - b.length);
  return similar.slice(0, 5);
}

module.exports = {
  fetchRegistry,
  resolveComponent,
  findSimilarPaths,
  getRegistryUrl,
  getRawBase,
  DEFAULT_REGISTRY_URL,
  DEFAULT_RAW_BASE
};
