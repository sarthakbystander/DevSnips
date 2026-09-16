/**
 * DevSnips CLI - Project context configuration management
 *
 * Manages the devsnips/config.json file which stores:
 * - Project context information
 * - Installed resource tracking
 *
 * config.json is CLI-managed: it is created when absent, read when present,
 * and updated automatically after successful installations. Unlike AGENTS.md
 * it MAY be rewritten by the CLI, but never destructively -- a malformed
 * existing file is treated as an error instead of being replaced.
 */

const fs = require('node:fs');
const path = require('node:path');

const CONFIG_FILENAME = 'config.json';
const CONFIG_VERSION = 1;

/**
 * Get the absolute path to the devsnips directory.
 *
 * Always derived from process.cwd(); callers never supply output directories,
 * which keeps the path fixed and inside the project security boundary.
 *
 * @returns {string} - Absolute path to the devsnips directory
 */
function getDevSnipsDirectory() {
  return path.join(process.cwd(), 'devsnips');
}

/**
 * Get the absolute path to the config.json file.
 *
 * @returns {string} - Absolute path to config.json
 */
function getConfigPath() {
  return path.join(getDevSnipsDirectory(), CONFIG_FILENAME);
}

/**
 * Ensure the devsnips directory exists.
 *
 * @returns {boolean} - True if the directory was created, false if it already existed
 */
function ensureDevSnipsDirectory() {
  const devsnipsDir = getDevSnipsDirectory();
  if (fs.existsSync(devsnipsDir)) {
    return false;
  }
  fs.mkdirSync(devsnipsDir, { recursive: true });
  return true;
}

/**
 * Create the default V1 config object.
 *
 * `resources` (rather than `components`) records every successful DevSnips
 * installation -- components, sections, and templates alike -- because the
 * registry installs any resolvable entry. Sections and templates are tracked
 * through the same record type.
 *
 * @returns {object} - Default config structure
 */
function createDefaultConfig() {
  return {
    version: CONFIG_VERSION,
    project: {},
    resources: []
  };
}

/**
 * Read and parse the config.json file.
 *
 * @returns {object|null} - Parsed config, or null if the file does not exist
 * @throws {Error} - If the file exists but is not valid JSON or not an object
 */
function readConfig() {
  const configPath = getConfigPath();

  if (!fs.existsSync(configPath)) {
    return null;
  }

  let config;
  try {
    const content = fs.readFileSync(configPath, 'utf8');
    config = JSON.parse(content);
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new Error(
        `config.json contains invalid JSON: ${error.message}. ` +
        'Fix or remove the file and re-run the command.'
      );
    }
    throw new Error(`Failed to read config.json: ${error.message}`);
  }

  if (config === null || typeof config !== 'object' || Array.isArray(config)) {
    throw new Error(
      'config.json must contain a JSON object. Fix or remove the file and re-run the command.'
    );
  }

  return config;
}

/**
 * Write config to config.json atomically (temp file + rename).
 *
 * Writing via a same-directory temporary file followed by rename means a
 * failed write never leaves truncated JSON at the config path, and works on
 * Windows where rename replaces existing files.
 *
 * @param {object} config - Config object to write
 * @throws {Error} - If the config cannot be written
 */
function writeConfig(config) {
  const configPath = getConfigPath();
  const dir = path.dirname(configPath);

  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Serialize with 2-space indentation and a trailing newline
  const content = JSON.stringify(config, null, 2) + '\n';

  const tempPath = configPath + '.tmp';
  let cleanupTemp = true;

  try {
    fs.writeFileSync(tempPath, content, 'utf8');
    fs.renameSync(tempPath, configPath);
    cleanupTemp = false;
  } catch (error) {
    // Surface a clear message and never leave a temp file behind
    throw new Error(`Failed to write config.json: ${error.message}`);
  } finally {
    if (cleanupTemp && fs.existsSync(tempPath)) {
      try {
        fs.unlinkSync(tempPath);
      } catch (cleanupError) {
        // Ignore cleanup errors
      }
    }
  }
}

/**
 * Ensure config.json exists, creating it if absent.
 *
 * @returns {object} - The config object (existing or newly created)
 * @throws {Error} - If the config exists but is malformed
 */
function ensureConfig() {
  const configPath = getConfigPath();

  if (fs.existsSync(configPath)) {
    // Read existing config - throws if malformed
    return readConfig();
  }

  const config = createDefaultConfig();
  ensureDevSnipsDirectory();
  writeConfig(config);
  return config;
}

/**
 * Record a newly installed resource in config.json.
 *
 * Only called after a resource has been successfully written to disk, so the
 * record always reflects a real installation rather than an attempt.
 *
 * @param {string} canonicalPath - Canonical registry path (e.g., "Vanilla/Components/Buttons/split-button")
 * @param {string} technology - Technology name from registry (e.g., "Vanilla HTML/CSS/JS")
 * @returns {boolean} - True if a record was added, false if the path was already recorded
 * @throws {Error} - If the config cannot be read/written
 */
function recordInstallation(canonicalPath, technology) {
  const config = ensureConfig();

  // Defensive duplicate protection: never create multiple identical records.
  const alreadyRecorded = (config.resources || []).some(
    r => r && r.path === canonicalPath
  );

  if (alreadyRecorded) {
    return false;
  }

  if (!Array.isArray(config.resources)) {
    config.resources = [];
  }

  config.resources.push({
    path: canonicalPath,
    technology: technology,
    installedAt: new Date().toISOString()
  });

  writeConfig(config);
  return true;
}

/**
 * Check if a resource is already recorded in config.
 *
 * @param {string} canonicalPath - Canonical registry path
 * @returns {boolean} - True if the resource is recorded
 */
function isResourceInstalled(canonicalPath) {
  const config = readConfig();
  if (!config) return false;
  return (config.resources || []).some(r => r && r.path === canonicalPath);
}

module.exports = {
  getDevSnipsDirectory,
  getConfigPath,
  ensureDevSnipsDirectory,
  createDefaultConfig,
  readConfig,
  writeConfig,
  ensureConfig,
  recordInstallation,
  isResourceInstalled
};
