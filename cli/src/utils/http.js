/**
 * DevSnips CLI - Shared HTTP fetch utility
 *
 * Single implementation of the GitHub Raw GET used by both the registry
 * resolver (JSON) and the file downloader (text), replacing two duplicated
 * hand-rolled https.get wrappers.
 */

const https = require('node:https');
const http = require('node:http');

const DEFAULT_TIMEOUT_MS = 30000;

/**
 * GET a URL and resolve with the response body as text.
 *
 * Both http: and https: URLs are supported; plain http exists for the
 * DEVSNIPS_REGISTRY_URL / DEVSNIPS_RAW_BASE overrides so tests, mirrors,
 * and offline setups can point at a local server. The built-in defaults
 * are always https.
 *
 * @param {string} url - URL to fetch
 * @param {object} [options]
 * @param {number} [options.timeoutMs] - Request timeout (default 30s)
 * @param {boolean} [options.rejectHtml] - Fail when the response is HTML
 *   (guards against GitHub error pages instead of real file content)
 * @returns {Promise<string>} - Response body
 */
function httpGetText(url, { timeoutMs = DEFAULT_TIMEOUT_MS, rejectHtml = false } = {}) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('http://') ? http : https;
    const req = client.get(url, (res) => {
      if (res.statusCode !== 200) {
        // Consume response to free socket
        res.resume();
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }

      if (rejectHtml && (res.headers['content-type'] || '').includes('text/html')) {
        res.resume();
        reject(new Error('Unexpected HTML response'));
        return;
      }

      let data = '';
      res.setEncoding('utf8');
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        resolve(data);
      });
    });

    req.on('error', reject);
    req.setTimeout(timeoutMs, () => {
      req.destroy();
      reject(new Error('Request timed out'));
    });
  });
}

module.exports = {
  httpGetText
};
