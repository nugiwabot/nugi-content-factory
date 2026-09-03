/* ============================================================
   Validasi konsistensi elemen antara demo HTML dan demo.js
   Jalankan: node website/demo/demo-elements.test.js
   ============================================================ */
'use strict';

const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const js = fs.readFileSync(path.join(__dirname, 'demo.js'), 'utf8');

const IDs = [
  'distLog', 'waCard', 'waAvatar', 'waHead', 'waBody', 'waMeta',
  'leadsTable', 'statsBox', 'btnSendLead', 'selectSource', 'btnReset', 'demoBanner'
];

let failures = 0;
for (const id of IDs) {
  const inHtml = new RegExp('id="' + id + '"').test(html);
  const inJs = js.indexOf("'" + id + "'") !== -1;
  const pass = inHtml && inJs;
  console.log((pass ? 'PASS' : 'FAIL') + ': element id "' + id + '" (html=' + inHtml + ', js=' + inJs + ')');
  if (!pass) failures += 1;
}

// Cek teks penting di HTML demo
const checks = [
  [/INTERACTIVE DEMO/, 'eyebrow INTERACTIVE DEMO'],
  [/MODE DEMO/, 'badge MODE DEMO'],
  [/Konsultasi Kebutuhan/, 'CTA konsultasi'],
  [/Kembali ke Website/, 'CTA kembali ke website'],
  [/Data simulasi/, 'label data simulasi']
];
for (const [re, label] of checks) {
  const pass = re.test(html);
  console.log((pass ? 'PASS' : 'FAIL') + ': ' + label);
  if (!pass) failures += 1;
}

console.log('\n' + (failures === 0 ? 'SEMUA CEK ELEMEN DEMO LULUS.' : failures + ' CEK GAGAL.'));
process.exit(failures === 0 ? 0 : 1);
