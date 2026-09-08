/**
 * DevSnips CLI - Registry resolver
 * 
 * Fetches and parses the snippets-index.json from the DevSnips repository
 * to resolve component paths to their canonical locations.
 */

const https = require('node:https');
const { exitWithNetworkError, exitWithError } = require('../utils/errors.js');

const REGISTRY_URL = 'https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/snippets-index.json';
const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/sarthakbystander/DevSnips/main/';

let cachedRegistry = null;

/**
 * Fetch JSON from a URL
 * 
 * @param {string} url - The URL to fetch
 * @returns {Promise<object>} - Parsed JSON response
 */
function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }

      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed);
        } catch (e) {
          reject(new Error('Invalid JSON response'));
        }
      });
    }).on('error', reject);
  });
}

/**
 * Fetch the registry from GitHub
 * 
 * @returns {Promise<object>} - The registry object
 */
async function fetchRegistry() {
  if (cachedRegistry) {
    return cachedRegistry;
  }

  try {
    const registry = await fetchJSON(REGISTRY_URL);
    
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
 * Normalize a path for comparison (strip trailing slashes, lowercase for matching)
 * 
 * @param {string} p - Path to normalize
 * @returns {string} - Normalized path
 */
function normalizeForMatch(p) {
  return p.toLowerCase().replace(/\/+$/, '');
}

/**
 * Resolve a user-provided path to a canonical component in the registry
 * 
 * @param {string} inputPath - User-provided path
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
      
      // Exact match
      if (normalizedVariant === normalizedInput) {
        return {
          family: family,
          variant: variant,
          canonicalPath: variantPath.replace(/\/+$/, ''),
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
 * Get the list of available variants for a partial path (for helpful error messages)
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
      if (normalizedVariant.startsWith(normalizedInput)) {
        similar.push(variantPath.replace(/\/+$/, ''));
      }
    }
  }
  
  return similar.slice(0, 5); // Return up to 5 suggestions
}

module.exports = {
  fetchRegistry,
  resolveComponent,
  findSimilarPaths,
  GITHUB_RAW_BASE
};
