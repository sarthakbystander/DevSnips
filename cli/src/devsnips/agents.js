/**
 * DevSnips CLI - AGENTS.md management
 *
 * Manages the root-level devsnips/AGENTS.md file which provides
 * project-wide instructions for AI coding agents working with
 * DevSnips resources.
 *
 * IMPORTANT: This file is user-editable and must NEVER be overwritten
 * once it exists.
 */

const fs = require('node:fs');
const path = require('node:path');

/**
 * Get the absolute path to the AGENTS.md file
 *
 * @returns {string} - Absolute path to AGENTS.md
 */
function getAgentsPath() {
  return path.join(process.cwd(), 'devsnips', 'AGENTS.md');
}

/**
 * Default content for AGENTS.md when created for the first time
 *
 * @returns {string} - Default AGENTS.md content
 */
function getDefaultAgentsContent() {
  return `# DevSnips Agent Instructions

This project uses DevSnips for UI resources.

## General Rules

When working with DevSnips resources:

- Inspect the existing project before modifying UI.
- Preserve the project's existing design language.
- Reuse existing project patterns and styles where appropriate.
- Do not introduce unnecessary dependencies.
- Keep UI responsive.
- Keep UI accessible.
- Avoid unnecessary duplication.
- Prefer the project's existing components and utilities when they already solve the problem.

## Resource Adaptation

DevSnips resources are starting points for this project.

When using an installed resource:

- Inspect the resource's README.md.
- Inspect its actual source files.
- Adapt the implementation to the project's existing conventions.
- Preserve intended functionality.
- Do not blindly copy implementation details when they conflict with the project's architecture.
- Reuse existing tokens, utilities, components, and patterns where appropriate.

## Quality Checks

Before considering an adapted DevSnips resource complete, verify:

- Responsive behavior
- Accessibility
- Keyboard interaction where applicable
- Focus states
- Hover and interaction states
- Color contrast
- Typography consistency
- Spacing consistency
- Overflow and text wrapping
- Semantic structure
- Unnecessary CSS or JavaScript
- Unnecessary dependencies

## Important

Do not modify this file automatically.

Project-specific instructions may be added below these defaults.
`;
}

/**
 * Ensure AGENTS.md exists, creating it only if it does not exist
 *
 * CRITICAL: If AGENTS.md already exists, it is left untouched.
 * This preserves any user customization.
 *
 * @returns {object} - { created: boolean, path: string }
 */
function ensureAgents() {
  const agentsPath = getAgentsPath();
  
  if (fs.existsSync(agentsPath)) {
    // File exists - do NOT overwrite
    return { created: false, path: agentsPath };
  }
  
  // File does not exist - create it
  const devsnipsDir = path.dirname(agentsPath);
  if (!fs.existsSync(devsnipsDir)) {
    fs.mkdirSync(devsnipsDir, { recursive: true });
  }
  
  const content = getDefaultAgentsContent();
  fs.writeFileSync(agentsPath, content, 'utf8');
  
  return { created: true, path: agentsPath };
}

/**
 * Check if AGENTS.md exists
 *
 * @returns {boolean} - True if AGENTS.md exists
 */
function agentsExists() {
  return fs.existsSync(getAgentsPath());
}

/**
 * Read the contents of AGENTS.md
 *
 * @returns {string|null} - Contents or null if not exists
 */
function readAgents() {
  const agentsPath = getAgentsPath();
  if (!fs.existsSync(agentsPath)) {
    return null;
  }
  return fs.readFileSync(agentsPath, 'utf8');
}

module.exports = {
  getAgentsPath,
  getDefaultAgentsContent,
  ensureAgents,
  agentsExists,
  readAgents
};
