/**
 * DevSnips CLI - Project context management
 *
 * High-level API for initializing and updating the DevSnips project context.
 * This includes ensuring the devsnips directory, config.json, and AGENTS.md
 * exist, and recording successful installations.
 */

const fs = require('node:fs');
const {
  ensureDevSnipsDirectory,
  ensureConfig,
  recordInstallation,
  getConfigPath
} = require('./config.js');
const { ensureAgents, getAgentsPath } = require('./agents.js');

/**
 * Initialize the DevSnips project context if it does not exist.
 *
 * This creates:
 * - ./devsnips/ directory
 * - ./devsnips/config.json (if missing)
 * - ./devsnips/AGENTS.md (if missing)
 *
 * Safe to run multiple times - existing files are never overwritten.
 *
 * @returns {object} - { agentsCreated: boolean, configCreated: boolean }
 */
function initializeContext() {
  ensureDevSnipsDirectory();

  // Determine whether config was created by this call (must check before)
  const configExisted = fs.existsSync(getConfigPath());
  ensureConfig();
  const configCreated = !configExisted;

  const agentsResult = ensureAgents();

  return {
    agentsCreated: agentsResult.created,
    configCreated: configCreated
  };
}

/**
 * Update the project context after a successful installation.
 *
 * Records the installed resource in config.json. Does NOT modify AGENTS.md
 * (user-owned file).
 *
 * @param {string} canonicalPath - Canonical registry path
 * @param {string} technology - Technology name from registry
 * @returns {boolean} - True if a record was added, false if it already existed
 * @throws {Error} - If the config cannot be read/written
 */
function updateContextAfterInstall(canonicalPath, technology) {
  return recordInstallation(canonicalPath, technology);
}

/**
 * Check if the DevSnips project context is initialized.
 *
 * @returns {boolean} - True if both config.json and AGENTS.md exist
 */
function isContextInitialized() {
  return fs.existsSync(getConfigPath()) && fs.existsSync(getAgentsPath());
}

module.exports = {
  initializeContext,
  updateContextAfterInstall,
  isContextInitialized
};
