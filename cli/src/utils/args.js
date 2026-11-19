/**
 * DevSnips CLI - Argument parsing helpers
 *
 * Pure functions so command wiring (cli/src/index.js) stays testable
 * without spawning processes.
 */

/**
 * Parse the arguments of the `add` command (everything after "add").
 *
 * @param {string[]} args - Raw arguments, e.g. ["React/...", "--force", "--dry-run"]
 * @returns {{ componentPath: string, force: boolean, dryRun: boolean } | { error: "missing-path" }}
 */
function parseAddCommand(args) {
  const force = args.includes('--force');
  const dryRun = args.includes('--dry-run');
  const componentPath = args.find(a => a !== 'add' && a !== '--force' && a !== '--dry-run');
  if (!componentPath) {
    return { error: 'missing-path' };
  }
  return { componentPath, force, dryRun };
}

module.exports = {
  parseAddCommand
};
