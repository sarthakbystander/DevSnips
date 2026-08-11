/**
 * Snippet Name: Debounced Input Handler (Js)
 * Description: Reusable debounced input handler (js) JavaScript utility snippet for frontend projects.
 * Author: DevSnips Contributors
 * Usage Example: Open `devsnips/snippets/js-snippets/Debounced Input Handler (JS).js` and copy the snippet into your project.
 */

function debounce(fn,ms=300){let t;return(...args)=>{clearTimeout(t);t=setTimeout(()=>fn(...args),ms);};}


// Usage
const onType=debounce(e=>console.log(e.target.value),350);
document.querySelector('#q').addEventListener('input',onType);