/**
 * DevSnips CLI - Project context management
 *
 * High-level API for initializing and updating the DevSnips project context.
 * This includes ensuring the devsnips directory, config.json, and AGENTS.md exist.
 */

const { ensureDevSnipsDirectory, ensureConfig, recordInstallation } = require('./config.js');
const { ensureAgents } = require('./agents.js');

/**
 * Initialize the DevSnips project context if it does not exist
 *
 * This creates:
 * - ./devsnips/ directory
 * - ./devsnips/config.json (if missing)
 * - ./devsnips/AGENTS.md (if missing)
 *
 * Safe to run multiple times - will not overwrite existing files.
 *
 * @returns {object} - { agentsCreated: boolean, configCreated: boolean }
 */
function initializeContext() {
  // Ensure directory exists
  ensureDevSnipsDirectory();
  
  // Check if config existed before ensureConfig
  const fs = require('node:fs');
  const path = require('node:path');
  const configPath = path.join(process.cwd(), 'devsnips', 'config.json');
  const configExisted = fs.existsSync(configPath);
  
  // Ensure config (creates if missing)
  ensureConfig();
  const configCreated = !configExisted;
  
  // Ensure AGENTS.md (creates only if missing)
  const agentsResult = ensureAgents();
  
  return {
    agentsCreated: agentsResult.created,
    configCreated: configCreated
  };
}

/**
 * Update the project context after a successful installation
 *
 * This records the installed resource in config.json.
 * Does NOT modify AGENTS.md (user-owned file).
 *
 * @param {string} canonicalPath - Canonical registry path
 * @param {string} technology - Technology name from registry
 * @returns {object} - { recorded: boolean, alreadyExisted: boolean }
 */
function updateContextAfterInstall(canonicalPath, technology) {
  try {
    const recorded = recordInstallation(canonicalPath, technology);
    return {
      recorded: recorded,
      alreadyExisted: !recorded
    };
  } catch (error) {
    // Re-throw to be handled by caller
    throw error;
  }
}

/**
 * Check if the DevSnips project context is initialized
 *
 * @returns {boolean} - True if both config.json and AGENTS.md exist
 */
function isContextInitialized() {
  const fs = require('node:fs');
  const path = require('node:path');
  
  const configPath = path.join(process.cwd(), 'devsnips', 'config.json');
  const agentsPath = path.join(process.cwd(), 'devsnips', 'AGENTS.md');
  
  return fs.existsSync(configPath) && fs.existsSync(agentsPath);
}

module.exports = {
  initializeContext,
  updateContextAfterInstall,
  isContextInitialized
};
