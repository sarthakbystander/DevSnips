/**
 * DevSnips CLI - File downloader
 * 
 * Downloads source files from the DevSnips GitHub repository.
 */

const https = require('node:https');
const { exitWithNetworkError } = require('../utils/errors.js');
const { GITHUB_RAW_BASE } = require('../registry/resolver.js');

/**
 * Download a file from GitHub Raw
 * 
 * @param {string} repoPath - Repository-relative path (e.g., "Tailwind/Components/...")
 * @returns {Promise<string>} - File contents
 */
function downloadFile(repoPath) {
  return new Promise((resolve, reject) => {
    const url = GITHUB_RAW_BASE + repoPath;
    
    https.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }

      // Check content type to avoid HTML error pages
      const contentType = res.headers['content-type'];
      if (contentType && contentType.includes('text/html')) {
        reject(new Error('Unexpected HTML response'));
      }

      let data = '';
      res.setEncoding('utf8');
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve(data);
      });
    }).on('error', reject);
  });
}

/**
 * Determine which files should be installed for a component
 * 
 * Based on DevSnips conventions:
 * - code.html, code.jsx, code.tsx are source files
 * - metadata.json is registry data (NOT installed)
 * - preview.html is for demonstration (NOT installed)
 * - README.md is documentation (optional, NOT installed by default)
 * - .css files may be source files for some components
 * 
 * @param {string[]} availableFiles - List of files in the component directory
 * @param {string} technology - Technology type
 * @returns {string[]} - Files to install
 */
function getSourceFiles(availableFiles, technology) {
  const sourceExtensions = ['.html', '.jsx', '.tsx', '.js', '.ts', '.css'];
  
  return availableFiles.filter(file => {
    // Never install metadata or preview files
    if (file === 'metadata.json') return false;
    if (file === 'preview.html') return false;
    if (file === 'README.md') return false;
    
    // Install source code files
    const ext = file.substring(file.lastIndexOf('.'));
    return sourceExtensions.includes(ext);
  });
}

/**
 * Build the full repository path for a file within a component
 * 
 * @param {string} componentPath - Canonical component path
 * @param {string} filename - Name of the file
 * @returns {string} - Full repository path
 */
function buildRepoFilePath(componentPath, filename) {
  // Ensure componentPath doesn't have trailing slash
  const base = componentPath.replace(/\/+$/, '');
  return `${base}/${filename}`;
}

module.exports = {
  downloadFile,
  getSourceFiles,
  buildRepoFilePath
};
