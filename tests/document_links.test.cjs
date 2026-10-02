// Exercise the search link guard without a browser or DOM.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync('js/document-search.js', 'utf8');
const fn = source.slice(source.indexOf('function documentHref('), source.indexOf('function formatReviewed('));
const context = vm.createContext({});
vm.runInContext(fn, context);
for (const url of ['/docs/kasapa-privacy', '../docs/parkmemory-support.html']) {
  assert.equal(context.documentHref(url), url);
  assert.equal(context.documentHref(url, 'getting-started'), url + '#getting-started');
}
for (const url of ['javascript:alert(1)', '//other.example/docs/a', '/docs/../secrets', '/docs/test?redirect=x']) {
  assert.equal(context.documentHref(url), '#');
}
assert.equal(context.documentHref('/docs/kasapa-privacy', 'bad anchor'), '/docs/kasapa-privacy');
console.log('9 search-link checks passed');
