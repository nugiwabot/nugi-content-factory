/* ============================================================
   Smoke test untuk DEMO SIMULASI (website/demo/demo.js)
   Jalankan: node website/demo/demo.test.js
   Memuat demo.js di sandbox Node (tanpa DOM) dan menguji
   logika inti: round-robin, status flow, dan ringkasan.
   ============================================================ */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const code = fs.readFileSync(path.join(__dirname, 'demo.js'), 'utf8');
const sandbox = { console };
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { filename: 'demo.js' });

const core = sandbox.NugiDemoCore;

let failures = 0;
function assert(cond, msg) {
  if (cond) {
    console.log('PASS: ' + msg);
  } else {
    failures += 1;
    console.error('FAIL: ' + msg);
  }
}

function reset() {
  core.reset();
  assert(core.getLeads().length === 0, 'reset mengosongkan leads');
}

// --- Test 1: round-robin menggilir sales secara adil ---
reset();
const seen = {};
for (let i = 0; i < 6; i++) {
  const lead = core.createLead('Meta Ads');
  core.assignToNextSales(lead);
  seen[lead.sales] = (seen[lead.sales] || 0) + 1;
}
assert(Object.keys(seen).length === 3, '3 sales menerima giliran');
assert(
  Object.values(seen).every((n) => n === 2),
  'distribusi merata (masing-masing 2 dari 6 lead)'
);

// --- Test 2: alur status Lead Baru -> ... -> Closing ---
reset();
const l = core.createLead('Landing Page');
assert(l.status === 'Lead Baru', 'lead baru berstatus "Lead Baru"');
const expected = ['Dihubungi', 'Survey Lokasi', 'Booking', 'Closing', 'Closing'];
expected.forEach((st, i) => {
  const after = core.advanceLead(l.id);
  assert(after.status === st, `advance ke-${i + 1} => ${st}`);
});

// --- Test 3: lead tidak tercatat dobel setelah advance terakhir ---
const summaryAtEnd = core.summary();
assert(summaryAtEnd.total === 1, 'total lead tetap 1 (tidak dobel)');
assert(summaryAtEnd.byStatus['Closing'] === 1, 'rekap status Closing benar');

// --- Test 4: assign menyimpan sales + timestamp ---
reset();
const l2 = core.createLead('Google Ads');
core.assignToNextSales(l2);
assert(l2.sales && l2.salesPhone, 'sales & nomor tersimpan di lead');
assert(/^0812-/.test(l2.phone), 'nomor prospek adalah nomor fiktif (prefix 0812-0000)');

// --- Test 5: data fiktif / tidak ada nama asli pribadi ---
const names = core.getLeads().map((x) => x.name);
reset();
assert(names.every((n) => /Contoh/i.test(n)), 'nama prospek selalu berlabel "Contoh"');

// --- Test 6: advanceLead pada id tak dikenal mengembalikan null ---
assert(core.advanceLead('L-999') === null, 'advanceLead id tak dikenal => null');

console.log('\n' + (failures === 0 ? 'SEMUA TEST LULUS.' : failures + ' TEST GAGAL.'));
process.exit(failures === 0 ? 0 : 1);
