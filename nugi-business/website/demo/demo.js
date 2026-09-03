/* ============================================================
   NUGIPROPERTI — DEMO SIMULASI ALUR LEADS (Client Demo)
   File: website/demo/demo.js
   Catatan: halaman ini adalah SIMULASI untuk presentasi.
   Bukan mesin produksi asli (mesin asli berada di repo terpisah).
   Data yang dipakai adalah data fiktif/berlabel "Contoh".
   ============================================================ */
(function (global) {
  'use strict';

  var STATUS_FLOW = ['Lead Baru', 'Dihubungi', 'Survey Lokasi', 'Booking', 'Closing'];

  // Data fiktif — jelas bukan orang/telepon nyata.
  var SALES = [
    { id: 's1', name: 'Sales A (Contoh)', phone: '0812-0000-0001' },
    { id: 's2', name: 'Sales B (Contoh)', phone: '0812-0000-0002' },
    { id: 's3', name: 'Sales C (Contoh)', phone: '0812-0000-0003' }
  ];

  var DUMMY_PROSPEK = [
    { name: 'Contoh: Bpk Andi', phone: '0812-0000-1001', note: 'Cari rumah 2 KT, budget 350jt' },
    { name: 'Contoh: Ibu Rina', phone: '0812-0000-1002', note: 'Tanya DP & cicilan' },
    { name: 'Contoh: Bpk Dedi', phone: '0812-0000-1003', note: 'Survey akhir pekan' },
    { name: 'Contoh: Ibu Sari', phone: '0812-0000-1004', note: 'Bandingkan 2 klaster' },
    { name: 'Contoh: Bpk Yoga', phone: '0812-0000-1005', note: 'Proses KPR' },
    { name: 'Contoh: Ibu Maya', phone: '0812-0000-1006', note: 'Booking unit' }
  ];

  var SOURCES = ['Meta Ads', 'Landing Page', 'Google Ads'];

  var state = { leads: [], rrIndex: 0, seq: 1 };

  function nextSales() {
    var s = SALES[state.rrIndex % SALES.length];
    state.rrIndex += 1;
    return s;
  }

  function createLead(source) {
    var src = SOURCES.indexOf(source) >= 0 ? source : SOURCES[0];
    var p = DUMMY_PROSPEK[(state.seq - 1) % DUMMY_PROSPEK.length];
    var lead = {
      id: 'L-' + state.seq,
      name: p.name,
      phone: p.phone,
      note: p.note,
      source: src,
      status: STATUS_FLOW[0],
      sales: null,
      salesPhone: null,
      createdAt: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
      assignedAt: null
    };
    state.seq += 1;
    state.leads.push(lead);
    return lead;
  }

  function assignToNextSales(lead) {
    var s = nextSales();
    lead.sales = s.name;
    lead.salesPhone = s.phone;
    lead.assignedAt = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
    return lead;
  }

  function advanceLead(id) {
    var lead = state.leads.find(function (l) { return l.id === id; });
    if (!lead) return null;
    var idx = STATUS_FLOW.indexOf(lead.status);
    if (idx >= 0 && idx < STATUS_FLOW.length - 1) {
      lead.status = STATUS_FLOW[idx + 1];
    }
    return lead;
  }

  function summary() {
    var byStatus = {};
    var bySales = {};
    STATUS_FLOW.forEach(function (st) { byStatus[st] = 0; });
    state.leads.forEach(function (l) {
      byStatus[l.status] = (byStatus[l.status] || 0) + 1;
      var key = l.sales || 'Belum Ada';
      bySales[key] = (bySales[key] || 0) + 1;
    });
    return { total: state.leads.length, byStatus: byStatus, bySales: bySales };
  }

  var core = {
    STATUS_FLOW: STATUS_FLOW,
    SALES: SALES,
    SOURCES: SOURCES,
    createLead: createLead,
    assignToNextSales: assignToNextSales,
    advanceLead: advanceLead,
    summary: summary,
    getLeads: function () { return state.leads; },
    reset: function () {
      state = { leads: [], rrIndex: 0, seq: 1 };
    }
  };

  global.NugiDemoCore = core;

  if (typeof document !== 'undefined' && document.getElementById) {
    initDemoUI(core);
  }

  /* ---------------- UI (hanya berjalan di browser) ---------------- */
  function initDemoUI(core) {
    var $ = function (id) { return document.getElementById(id); };

    var elLog = $('distLog');
    var elWaCard = $('waCard');
    var elWaHead = $('waHead');
    var elWaAvatar = $('waAvatar');
    var elWaBody = $('waBody');
    var elWaMeta = $('waMeta');
    var elTable = $('leadsTable');
    var elStats = $('statsBox');
    var elBtnSend = $('btnSendLead');
    var elSource = $('selectSource');
    var elReset = $('btnReset');
    var elBanner = $('demoBanner');

    function fmtStatus(s) { return '<span class="st ' + s.replace(/\s+/g, '-').toLowerCase() + '">' + s + '</span>'; }

    function initials(name) {
      var parts = String(name || '').replace(/[^a-zA-Z ]/g, '').trim().split(/\s+/);
      var a = (parts[0] || 'S').charAt(0);
      var b = parts.length > 1 ? parts[parts.length - 1].charAt(0) : '';
      return (a + b).toUpperCase();
    }

    function renderDist(lead) {
      elLog.innerHTML =
        'Lead <b>' + lead.id + '</b> masuk dari <b>' + lead.source + '</b> (' + lead.createdAt + ')' +
        ' &rarr; didistribusikan ke <b>' + lead.sales + '</b> pukul ' + lead.assignedAt + '.';
    }

    function renderWa(lead) {
      elWaCard.hidden = false;
      elWaAvatar.textContent = initials(lead.sales);
      elWaHead.textContent = lead.sales + ' — WhatsApp';
      elWaBody.innerHTML =
        '<p><b>' + lead.name + '</b></p>' +
        '<p>Telepon: ' + lead.phone + '</p>' +
        '<p>Catatan: ' + lead.note + '</p>' +
        '<p>Sumber: ' + lead.source + ' &middot; Masuk: ' + lead.createdAt + '</p>';
      elWaMeta.textContent = 'Notifikasi terkirim ke ' + lead.salesPhone + ' dalam <10 detik (simulasi).';
    }

    function renderTable() {
      var leads = core.getLeads();
      if (leads.length === 0) {
        elTable.innerHTML = '<tr><td colspan="6">Belum ada lead. Klik "Simulasi Lead Baru" di atas.</td></tr>';
        return;
      }
      var html = '';
      leads.forEach(function (l) {
        html +=
          '<tr>' +
          '<td>' + l.id + '</td>' +
          '<td>' + l.name + '</td>' +
          '<td>' + l.source + '</td>' +
          '<td>' + (l.sales || '—') + '</td>' +
          '<td>' + fmtStatus(l.status) + '</td>' +
          '<td><button class="btn-mini" data-advance="' + l.id + '"' + (l.status === 'Closing' ? ' disabled' : '') + '>Lanjut &raquo;</button></td>' +
          '</tr>';
      });
      elTable.innerHTML = html;
    }

    function renderStats() {
      var s = core.summary();
      if (s.total === 0) {
        elStats.innerHTML = '<p class="muted">Belum ada data. Mulai dengan simulasi lead pertama.</p>';
        return;
      }

      var leadBaru = s.byStatus['Lead Baru'] || 0;
      var dihubungi = s.byStatus['Dihubungi'] || 0;
      var survey = s.byStatus['Survey Lokasi'] || 0;
      var booking = s.byStatus['Booking'] || 0;
      var closing = s.byStatus['Closing'] || 0;

      var html =
        '<div class="metric-grid">' +
        '<div class="metric-card"><div class="m-value">' + s.total + '</div><div class="m-label">Lead Total</div></div>' +
        '<div class="metric-card"><div class="m-value">' + (leadBaru + dihubungi) + '</div><div class="m-label">Dalam Follow-Up</div></div>' +
        '<div class="metric-card"><div class="m-value">' + survey + '</div><div class="m-label">Survey</div></div>' +
        '<div class="metric-card"><div class="m-value">' + booking + '</div><div class="m-label">Booking</div></div>' +
        '<div class="metric-card"><div class="m-value">' + closing + '</div><div class="m-label">Closing</div></div>' +
        '</div>';

      html += '<p>Per Status: ';
      Object.keys(s.byStatus).forEach(function (k) {
        if (s.byStatus[k] > 0) html += fmtStatus(k) + ' &times;' + s.byStatus[k] + ' ';
      });
      html += '</p>';
      html += '<p>Per Sales: ';
      Object.keys(s.bySales).forEach(function (k) { html += '<b>' + k + '</b>: ' + s.bySales[k] + ' &middot; '; });
      html += '</p>';

      elStats.innerHTML = html;
    }

    function renderAll() {
      renderTable();
      renderStats();
    }

    elBtnSend.addEventListener('click', function () {
      var lead = core.createLead(elSource.value);
      core.assignToNextSales(lead);
      renderDist(lead);
      renderWa(lead);
      renderAll();
    });

    elTable.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-advance]');
      if (!btn) return;
      core.advanceLead(btn.getAttribute('data-advance'));
      renderAll();
    });

    elReset.addEventListener('click', function () {
      core.reset();
      elLog.textContent = 'Menunggu simulasi lead pertama…';
      elWaCard.hidden = true;
      renderAll();
    });

    elBanner.textContent = 'MODE DEMO · Data simulasi (bukan data asli) · Klik "Simulasi Lead Baru" untuk memulai';
    renderAll();
  }
})(typeof window !== 'undefined' ? window : globalThis);
