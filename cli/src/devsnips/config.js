/**
 * DevSnips CLI - Project context configuration management
 *
 * Manages the devsnips/config.json file which stores:
 * - Project context information
 * - Installed resources tracking
 */

const fs = require('node:fs');
const path = require('node:path');

/**
 * Get the absolute path to the config.json file
 *
 * @returns {string} - Absolute path to config.json
 */
function getConfigPath() {
  return path.join(process.cwd(), 'devsnips', 'config.json');
}

/**
 * Ensure the devsnips directory exists
 */
function ensureDevSnipsDirectory() {
  const devsnipsDir = path.join(process.cwd(), 'devsnips');
  if (!fs.existsSync(devsnipsDir)) {
    fs.mkdirSync(devsnipsDir, { recursive: true });
  }
}

/**
 * Create a default empty config object
 *
 * @returns {object} - Default config structure
 */
function createDefaultConfig() {
  return {
    version: 1,
    project: {},
    resources: []
  };
}

/**
 * Read and parse the config.json file
 *
 * @returns {object|null} - Parsed config or null if not exists
 * @throws {Error} - If config exists but is malformed JSON
 */
function readConfig() {
  const configPath = getConfigPath();
  
  if (!fs.existsSync(configPath)) {
    return null;
  }
  
  try {
    const content = fs.readFileSync(configPath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new Error(`config.json contains invalid JSON: ${error.message}`);
    }
    throw error;
  }
}

/**
 * Write config to config.json atomically (temp file + rename)
 *
 * @param {object} config - Config object to write
 */
function writeConfig(config) {
  const configPath = getConfigPath();
  const dir = path.dirname(configPath);
  
  // Ensure directory exists
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // Serialize with 2-space indentation and trailing newline
  const content = JSON.stringify(config, null, 2) + '\n';
  
  // Write to temporary file first, then rename for atomicity
  const tempPath = configPath + '.tmp';
  
  try {
    fs.writeFileSync(tempPath, content, 'utf8');
    fs.renameSync(tempPath, configPath);
  } catch (error) {
    // Clean up temp file if it exists
    try {
      if (fs.existsSync(tempPath)) {
        fs.unlinkSync(tempPath);
      }
    } catch (cleanupError) {
      // Ignore cleanup errors
    }
    throw error;
  }
}

/**
 * Ensure config.json exists, creating it if necessary
 *
 * @returns {object} - The config object (existing or newly created)
 * @throws {Error} - If config exists but is malformed
 */
function ensureConfig() {
  const configPath = getConfigPath();
  
  if (fs.existsSync(configPath)) {
    // Read existing config - will throw if malformed
    return readConfig();
  }
  
  // Create new default config
  const config = createDefaultConfig();
  ensureDevSnipsDirectory();
  writeConfig(config);
  return config;
}

/**
 * Record a newly installed resource in config.json
 *
 * @param {string} canonicalPath - Canonical registry path (e.g., "Vanilla/Components/Buttons/split-button")
 * @param {string} technology - Technology name from registry (e.g., "Vanilla HTML/CSS/JS")
 * @returns {boolean} - True if record was added, false if already existed
 * @throws {Error} - If config cannot be read/written
 */
function recordInstallation(canonicalPath, technology) {
  const config = ensureConfig();
  
  // Check if this resource is already recorded
  const existingIndex = config.resources.findIndex(
    r => r.path === canonicalPath
  );
  
  if (existingIndex !== -1) {
    // Already recorded, do not duplicate
    return false;
  }
  
  // Add new installation record
  config.resources.push({
    path: canonicalPath,
    technology: technology,
    installedAt: new Date().toISOString()
  });
  
  writeConfig(config);
  return true;
}

/**
 * Check if a resource is already recorded in config
 *
 * @param {string} canonicalPath - Canonical registry path
 * @returns {boolean} - True if resource is recorded
 */
function isResourceInstalled(canonicalPath) {
  try {
    const config = readConfig();
    if (!config) return false;
    return config.resources.some(r => r.path === canonicalPath);
  } catch (error) {
    return false;
  }
}

module.exports = {
  getConfigPath,
  ensureDevSnipsDirectory,
  createDefaultConfig,
  readConfig,
  writeConfig,
  ensureConfig,
  recordInstallation,
  isResourceInstalled
};
