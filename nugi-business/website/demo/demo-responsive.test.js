/* ============================================================
   Validasi responsive & link internal halaman demo
   Jalankan: node website/demo/demo-responsive.test.js
   ============================================================ */
'use strict';

const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname);
const html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
const css = fs.readFileSync(path.join(dir, 'demo.css'), 'utf8');

const checks = [
  [css, /@media \(max-width: 640px\)/, 'CSS memiliki breakpoint mobile 640px'],
  [css, /.table-wrap \{\s*overflow-x:\s*auto/, 'tabel dibungkus scroll horizontal (tidak overflow halaman)'],
  [css, /repeat\(auto-fit, minmax\(140px, 1fr\)\)/, 'metric grid responsif (auto-fit)'],
  [css, /.demo-flow/, 'flow indicator ada di CSS'],
  [css, /.metric-card/, 'metric card ada di CSS'],
  [html, /href="\.\.\/"/, 'navbar memuat link kembali ke website'],
  [html, /href="\.\.\/#konsultasi"/, 'navbar memuat CTA konsultasi'],
  [html, /wa\.me\/6287747584665/, 'CTA bawah memakai nomor WhatsApp existing'],
  [html, /id="leadsTable"/, 'tabel leads ada di HTML']
];

let failures = 0;
for (const [content, re, label] of checks) {
  const pass = re.test(content);
  console.log((pass ? 'PASS' : 'FAIL') + ': ' + label);
  if (!pass) failures += 1;
}

if (/min-width:\s*9\d\d/.test(css)) {
  failures += 1;
  console.error('FAIL: ditemukan min-width >=900 di demo.css');
} else {
  console.log('PASS: tidak ada min-width besar yang memaksa horizontal overflow');
}

console.log('\n' + (failures === 0 ? 'SEMUA CEK RESPONSIVE DEMO LULUS.' : failures + ' CEK GAGAL.'));
process.exit(failures === 0 ? 0 : 1);
