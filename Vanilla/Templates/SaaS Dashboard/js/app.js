/* ============================================================
   Northstar — SaaS Dashboard shared application script
   Vanilla JS. Loaded by every page in the template.
   Responsibilities:
     1. Coherent mock SaaS dataset (DB) shared across all pages.
     2. App-shell render (NAV config) + theme + sidebar + toast.
     3. Shared helpers: fmt/money/compact/svg icons/pills/avatars.
     4. Chart utilities: sparkline, line chart, bar chart, donut.
     5. Reusable components: pagination, modal, drawer, confirm,
        toggle, skeleton, empty/error states, tabs, breadcrumbs.
   ============================================================ */
(function () {
  'use strict';

  var root = document.documentElement;

  /* =====================================================================
     ICONS — inline SVG strings (stroke = currentColor)
  ===================================================================== */
  var ICONS = {
    dashboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>',
    analytics: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l4-4 4 3 5-6"/></svg>',
    reports: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>',
    activity: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
    inbox: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 5.5L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.5-6.5A2 2 0 0 0 16.5 4h-9a2 2 0 0 0-1.8 1.5z"/></svg>',
    customers: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    segments: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10H12V2z"/><path d="M12 12L2 12"/></svg>',
    invitations: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    billing: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>',
    plans: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    card: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/></svg>',
    invoices: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13l2 2 4-4"/></svg>',
    transactions: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 10l5-5 5 5M7 14l5 5 5-5"/></svg>',
    notifications: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    team: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    roles: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    workspace: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg>',
    integrations: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="9" height="9"/><rect x="13" y="2" width="9" height="9"/><rect x="2" y="13" width="9" height="9"/><line x1="22" y1="13" x2="22" y2="22"/><line x1="16" y1="16" x2="22" y2="16"/><line x1="16" y1="22" x2="22" y2="22"/><line x1="13" y1="13" x2="13" y2="22"/></svg>',
    settings: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    profile: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    security: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    sessions: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>',
    api: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    webhooks: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 16.98h-5.99c-1.1 0-1.95.94-2.48 1.9A4 4 0 0 1 2 17c.01-.7.2-1.4.57-2"/><path d="M6 17l3.13-5.78c.53-.97.1-2.18-.5-3.1a4 4 0 1 1 6.89-4.06"/><path d="M12 6l3.13 5.73C15.66 12.7 16.9 13 18 13a4 4 0 0 1 0 8"/></svg>',
    help: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3M12 17h.01"/></svg>',
    support: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    status: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 12h18M3 6h18M3 18h18"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>',
    bell: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    chevronRight: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>',
    chevronDown: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>',
    plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>',
    download: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>',
    export: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>',
    eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
    edit: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>',
    trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>',
    more: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>',
    checkCircle: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4L12 14.01l-3-3"/></svg>',
    alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    xCircle: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/></svg>',
    inboxEmpty: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 5.5L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.5-6.5A2 2 0 0 0 16.5 4h-9a2 2 0 0 0-1.8 1.5z"/></svg>',
    doc: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>',
    filter: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>',
    calendar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    refresh: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 4v6h-6M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
    mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    send: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
    reply: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 17 4 12 9 7"/><path d="M20 18v-2a4 4 0 0 0-4-4H4"/></svg>',
    copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
    key: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.778-7.778zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>',
    lock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    arrowUp: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17l5-5 5 5M7 7h10"/></svg>',
    arrowDown: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7l5 5 5-5M7 17h10"/></svg>',
    arrowLeft: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>',
    external: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>',
    package: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
    user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    globe: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    star: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
  };

  /* =====================================================================
     NAVIGATION CONFIG — single source of truth for the sidebar.
     Every entry points to a real page in pages/. No dead links.
  ===================================================================== */
  var NAV = [
    { group: 'Overview', items: [
      { id: 'dashboard', label: 'Dashboard', href: 'dashboard.html', icon: 'dashboard' },
      { id: 'analytics', label: 'Analytics', href: 'analytics.html', icon: 'analytics' },
      { id: 'reports', label: 'Reports', href: 'reports.html', icon: 'reports' },
      { id: 'activity', label: 'Activity', href: 'activity.html', icon: 'activity' }
    ]},
    { group: 'Customers', items: [
      { id: 'customers', label: 'Customers', href: 'customers.html', icon: 'customers' },
      { id: 'customer-segments', label: 'Segments', href: 'customer-segments.html', icon: 'segments' },
      { id: 'invitations', label: 'Invitations', href: 'invitations.html', icon: 'invitations' }
    ]},
    { group: 'Revenue', items: [
      { id: 'billing', label: 'Billing', href: 'billing.html', icon: 'billing' },
      { id: 'plans', label: 'Plans', href: 'plans.html', icon: 'plans' },
      { id: 'payment-methods', label: 'Payment methods', href: 'payment-methods.html', icon: 'card' },
      { id: 'invoices', label: 'Invoices', href: 'invoices.html', icon: 'invoices' },
      { id: 'transactions', label: 'Transactions', href: 'transactions.html', icon: 'transactions' }
    ]},
    { group: 'Communication', items: [
      { id: 'inbox', label: 'Inbox', href: 'inbox.html', icon: 'inbox', count: 4 },
      { id: 'notifications', label: 'Notifications', href: 'notifications.html', icon: 'notifications' }
    ]},
    { group: 'Workspace', items: [
      { id: 'team', label: 'Team', href: 'team.html', icon: 'team' },
      { id: 'roles', label: 'Roles & permissions', href: 'roles.html', icon: 'roles' },
      { id: 'integrations', label: 'Integrations', href: 'integrations.html', icon: 'integrations' },
      { id: 'workspace-settings', label: 'Workspace', href: 'workspace-settings.html', icon: 'workspace' }
    ]},
    { group: 'Settings', items: [
      { id: 'settings', label: 'General', href: 'settings.html', icon: 'settings' },
      { id: 'profile', label: 'Profile', href: 'profile.html', icon: 'profile' },
      { id: 'security', label: 'Security', href: 'security.html', icon: 'security' },
      { id: 'sessions', label: 'Sessions', href: 'sessions.html', icon: 'sessions' },
      { id: 'api-keys', label: 'API', href: 'api-keys.html', icon: 'api' },
      { id: 'webhooks', label: 'Webhooks', href: 'webhooks.html', icon: 'webhooks' }
    ]},
    { group: 'Support', items: [
      { id: 'help-center', label: 'Help center', href: 'help-center.html', icon: 'help' },
      { id: 'support', label: 'Support', href: 'support.html', icon: 'support' },
      { id: 'system-status', label: 'System status', href: 'system-status.html', icon: 'status' }
    ]}
  ];

  var SETTINGS_NAV = [
    { id: 'settings', label: 'General', href: 'settings.html', icon: 'settings' },
    { id: 'profile', label: 'Profile', href: 'profile.html', icon: 'profile' },
    { id: 'security', label: 'Security', href: 'security.html', icon: 'security' },
    { id: 'sessions', label: 'Sessions', href: 'sessions.html', icon: 'sessions' },
    { id: 'preferences', label: 'Preferences', href: 'preferences.html', icon: 'dashboard' },
    { id: 'api-keys', label: 'API keys', href: 'api-keys.html', icon: 'api' },
    { id: 'webhooks', label: 'Webhooks', href: 'webhooks.html', icon: 'webhooks' },
    { id: 'integrations', label: 'Integrations', href: 'integrations.html', icon: 'integrations' }
  ];

  /* =====================================================================
     COHERENT MOCK SaaS DATASET (DB)
     Customers, team, invoices, transactions, activity, conversations,
     notifications all reference the same entities so data is consistent
     across every page.
  ===================================================================== */
  var TONES = { indigo: '#4f46e5', emerald: '#10b981', sky: '#0ea5e9', violet: '#8b5cf6', amber: '#f59e0b', rose: '#ef4444', teal: '#14b8a6', orange: '#f97316', blue: '#3b82f6', pink: '#ec4899' };

  var TEAM = [
    { id: 'u1', name: 'Alex Morgan', email: 'alex@northstar.io', initials: 'AM', tone: TONES.indigo, role: 'Owner', status: 'active', last: 'Online now', joined: 'Jan 2023', twoFactor: true },
    { id: 'u2', name: 'Maya Andersson', email: 'maya@northstar.io', initials: 'MA', tone: TONES.emerald, role: 'Admin', status: 'active', last: '12 min ago', joined: 'Mar 2023', twoFactor: true },
    { id: 'u3', name: 'Priya Raman', email: 'priya@northstar.io', initials: 'PR', tone: TONES.sky, role: 'Manager', status: 'active', last: '1 hour ago', joined: 'Jun 2023', twoFactor: true },
    { id: 'u4', name: 'Jonas Lee', email: 'jonas@northstar.io', initials: 'JL', tone: TONES.violet, role: 'Member', status: 'active', last: '3 hours ago', joined: 'Aug 2023', twoFactor: false },
    { id: 'u5', name: 'Sara Yilmaz', email: 'sara@northstar.io', initials: 'SY', tone: TONES.pink, role: 'Member', status: 'active', last: 'Yesterday', joined: 'Oct 2023', twoFactor: true },
    { id: 'u6', name: 'Diego Costa', email: 'diego@northstar.io', initials: 'DC', tone: TONES.amber, role: 'Viewer', status: 'invited', last: '—', joined: '—', twoFactor: false },
    { id: 'u7', name: 'Ava Nilsson', email: 'ava@northstar.io', initials: 'AN', tone: TONES.teal, role: 'Member', status: 'active', last: '2 days ago', joined: 'Feb 2024', twoFactor: true },
    { id: 'u8', name: 'Theo Faroe', email: 'theo@northstar.io', initials: 'TF', tone: TONES.rose, role: 'Viewer', status: 'suspended', last: '5 days ago', joined: 'Apr 2024', twoFactor: false }
  ];

  var CUSTOMERS = [
    { id: 'c1', name: 'Maya Andersson', company: 'Northwind', email: 'maya@northwind.io', initials: 'MA', tone: TONES.indigo, plan: 'Scale', status: 'active', mrr: 840, arr: 10080, signup: '2023-03-14', lastActive: '2 min ago', country: 'Sweden', seat: 12, notes: 'Expanding team next quarter. Upsell to Enterprise likely.' },
    { id: 'c2', name: 'Priya Raman', company: 'Kepler Co.', email: 'priya@keplerco.com', initials: 'PR', tone: TONES.emerald, plan: 'Scale', status: 'active', mrr: 840, arr: 10080, signup: '2023-06-02', lastActive: '14 min ago', country: 'India', seat: 8, notes: 'Strong advocate. Case study candidate.' },
    { id: 'c3', name: 'Jonas Lee', company: 'Bright Labs', email: 'jonas@brightlabs.dev', initials: 'JL', tone: TONES.sky, plan: 'Growth', status: 'trial', mrr: 240, arr: 2880, signup: '2024-07-21', lastActive: '38 min ago', country: 'Singapore', seat: 5, notes: 'On trial — needs onboarding push.' },
    { id: 'c4', name: 'Sara Yilmaz', company: 'Altapine', email: 'sara@altapine.co', initials: 'SY', tone: TONES.violet, plan: 'Scale', status: 'active', mrr: 840, arr: 10080, signup: '2023-10-11', lastActive: '2 hours ago', country: 'Turkey', seat: 9, notes: '' },
    { id: 'c5', name: 'Diego Costa', company: 'Summit App', email: 'diego@summit.app', initials: 'DC', tone: TONES.amber, plan: 'Starter', status: 'trial', mrr: 49, arr: 588, signup: '2024-08-05', lastActive: '4 hours ago', country: 'Brazil', seat: 2, notes: 'Trial expires in 9 days.' },
    { id: 'c6', name: 'Ava Nilsson', company: 'Vantage', email: 'ava@vantage.io', initials: 'AN', tone: TONES.teal, plan: 'Scale', status: 'active', mrr: 1160, arr: 13920, signup: '2023-01-28', lastActive: '5 hours ago', country: 'Norway', seat: 14, notes: 'Highest ARR account. VIP support tier.' },
    { id: 'c7', name: 'Theo Faroe', company: 'Altapine', email: 'theo@altapine.co', initials: 'TF', tone: TONES.rose, plan: 'Growth', status: 'pastdue', mrr: 240, arr: 2880, signup: '2023-09-17', lastActive: '1 day ago', country: 'Denmark', seat: 4, notes: 'Card declined. Dunning emails sent.' },
    { id: 'c8', name: 'Liam Chen', company: 'Orbit', email: 'liam@orbit.dev', initials: 'LC', tone: TONES.blue, plan: 'Growth', status: 'active', mrr: 240, arr: 2880, signup: '2024-02-13', lastActive: '1 day ago', country: 'Canada', seat: 6, notes: '' },
    { id: 'c9', name: 'Noor Aziz', company: 'Meridian', email: 'noor@meridian.co', initials: 'NA', tone: TONES.pink, plan: 'Scale', status: 'active', mrr: 840, arr: 10080, signup: '2023-11-30', lastActive: '2 days ago', country: 'UAE', seat: 11, notes: '' },
    { id: 'c10', name: 'Elena Vasquez', company: 'Helix', email: 'elena@helix.io', initials: 'EV', tone: TONES.orange, plan: 'Starter', status: 'active', mrr: 49, arr: 588, signup: '2024-05-19', lastActive: '2 days ago', country: 'Spain', seat: 1, notes: '' },
    { id: 'c11', name: 'Marcus Webb', company: 'Vertex', email: 'marcus@vertex.app', initials: 'MW', tone: TONES.amber, plan: 'Trial', status: 'trial', mrr: 0, arr: 0, signup: '2024-08-08', lastActive: '3 days ago', country: 'UK', seat: 3, notes: 'Evaluating vs competitor.' },
    { id: 'c12', name: 'Yuki Tanaka', company: 'Lumen', email: 'yuki@lumen.dev', initials: 'YT', tone: TONES.indigo, plan: 'Growth', status: 'active', mrr: 240, arr: 2880, signup: '2024-03-22', lastActive: '3 days ago', country: 'Japan', seat: 5, notes: '' },
    { id: 'c13', name: 'Omar Haddad', company: 'Cedar Works', email: 'omar@cedarworks.co', initials: 'OH', tone: TONES.emerald, plan: 'Scale', status: 'active', mrr: 840, arr: 10080, signup: '2023-07-04', lastActive: '4 days ago', country: 'Lebanon', seat: 10, notes: '' },
    { id: 'c14', name: 'Clara Berg', company: 'Fjord Studio', email: 'clara@fjord.studio', initials: 'CB', tone: TONES.sky, plan: 'Starter', status: 'active', mrr: 49, arr: 588, signup: '2024-06-12', lastActive: '5 days ago', country: 'Iceland', seat: 1, notes: '' },
    { id: 'c15', name: 'Ravi Patel', company: 'Orbit', email: 'ravi@orbit.dev', initials: 'RP', tone: TONES.violet, plan: 'Growth', status: 'active', mrr: 240, arr: 2880, signup: '2024-01-09', lastActive: '6 days ago', country: 'India', seat: 6, notes: '' },
    { id: 'c16', name: 'Hana Kim', company: 'Bright Labs', email: 'hana@brightlabs.dev', initials: 'HK', tone: TONES.rose, plan: 'Growth', status: 'pastdue', mrr: 240, arr: 2880, signup: '2023-12-03', lastActive: '1 week ago', country: 'South Korea', seat: 5, notes: 'Reach out about renewal.' },
    { id: 'c17', name: 'Lucas Moreau', company: 'Kepler Co.', email: 'lucas@keplerco.com', initials: 'LM', tone: TONES.teal, plan: 'Starter', status: 'active', mrr: 49, arr: 588, signup: '2024-04-27', lastActive: '1 week ago', country: 'France', seat: 2, notes: '' },
    { id: 'c18', name: 'Ingrid Olsen', company: 'Vantage', email: 'ingrid@vantage.io', initials: 'IO', tone: TONES.blue, plan: 'Scale', status: 'active', mrr: 840, arr: 10080, signup: '2023-05-18', lastActive: '1 week ago', country: 'Sweden', seat: 13, notes: '' }
  ];

  var INVOICES = [
    { id: 'INV-2043', customer: 'c2', customerName: 'Priya Raman', company: 'Kepler Co.', amount: 240.00, status: 'paid', date: '2026-08-11', due: '2026-08-11', plan: 'Scale' },
    { id: 'INV-2042', customer: 'c1', customerName: 'Maya Andersson', company: 'Northwind', amount: 840.00, status: 'paid', date: '2026-08-11', due: '2026-08-11', plan: 'Scale' },
    { id: 'INV-2041', customer: 'c3', customerName: 'Jonas Lee', company: 'Bright Labs', amount: 240.00, status: 'pending', date: '2026-08-10', due: '2026-08-17', plan: 'Growth' },
    { id: 'INV-2040', customer: 'c4', customerName: 'Sara Yilmaz', company: 'Altapine', amount: 840.00, status: 'paid', date: '2026-08-10', due: '2026-08-10', plan: 'Scale' },
    { id: 'INV-2039', customer: 'c7', customerName: 'Theo Faroe', company: 'Altapine', amount: 240.00, status: 'failed', date: '2026-08-09', due: '2026-08-09', plan: 'Growth' },
    { id: 'INV-2038', customer: 'c6', customerName: 'Ava Nilsson', company: 'Vantage', amount: 1160.00, status: 'paid', date: '2026-08-09', due: '2026-08-09', plan: 'Scale' },
    { id: 'INV-2037', customer: 'c8', customerName: 'Liam Chen', company: 'Orbit', amount: 240.00, status: 'paid', date: '2026-08-08', due: '2026-08-08', plan: 'Growth' },
    { id: 'INV-2036', customer: 'c9', customerName: 'Noor Aziz', company: 'Meridian', amount: 840.00, status: 'refunded', date: '2026-08-07', due: '2026-08-07', plan: 'Scale' },
    { id: 'INV-2035', customer: 'c10', customerName: 'Elena Vasquez', company: 'Helix', amount: 49.00, status: 'paid', date: '2026-08-06', due: '2026-08-06', plan: 'Starter' },
    { id: 'INV-2034', customer: 'c12', customerName: 'Yuki Tanaka', company: 'Lumen', amount: 240.00, status: 'paid', date: '2026-08-05', due: '2026-08-05', plan: 'Growth' },
    { id: 'INV-2033', customer: 'c13', customerName: 'Omar Haddad', company: 'Cedar Works', amount: 840.00, status: 'paid', date: '2026-08-04', due: '2026-08-04', plan: 'Scale' },
    { id: 'INV-2032', customer: 'c16', customerName: 'Hana Kim', company: 'Bright Labs', amount: 240.00, status: 'overdue', date: '2026-07-28', due: '2026-07-28', plan: 'Growth' }
  ];

  var TRANSACTIONS = [
    { id: 'txn_01H8K', invoice: 'INV-2043', customer: 'c2', customerName: 'Priya Raman', amount: 240.00, status: 'paid', date: '2026-08-11 14:22', method: 'Visa •• 4242', plan: 'Scale' },
    { id: 'txn_01H8J', invoice: 'INV-2042', customer: 'c1', customerName: 'Maya Andersson', amount: 840.00, status: 'paid', date: '2026-08-11 09:14', method: 'Visa •• 4242', plan: 'Scale' },
    { id: 'txn_01H8H', invoice: 'INV-2041', customer: 'c3', customerName: 'Jonas Lee', amount: 240.00, status: 'pending', date: '2026-08-10 18:40', method: 'Awaiting payment', plan: 'Growth' },
    { id: 'txn_01H8G', invoice: 'INV-2040', customer: 'c4', customerName: 'Sara Yilmaz', amount: 840.00, status: 'paid', date: '2026-08-10 11:02', method: 'MC •• 5519', plan: 'Scale' },
    { id: 'txn_01H8F', invoice: 'INV-2039', customer: 'c7', customerName: 'Theo Faroe', amount: 240.00, status: 'failed', date: '2026-08-09 22:18', method: 'Visa •• 1881', plan: 'Growth' },
    { id: 'txn_01H8E', invoice: 'INV-2038', customer: 'c6', customerName: 'Ava Nilsson', amount: 1160.00, status: 'paid', date: '2026-08-09 08:55', method: 'Amex •• 1007', plan: 'Scale' },
    { id: 'txn_01H8D', invoice: 'INV-2037', customer: 'c8', customerName: 'Liam Chen', amount: 240.00, status: 'paid', date: '2026-08-08 13:30', method: 'Visa •• 7781', plan: 'Growth' },
    { id: 'txn_01H8C', invoice: 'INV-2036', customer: 'c9', customerName: 'Noor Aziz', amount: 840.00, status: 'refunded', date: '2026-08-07 16:12', method: 'MC •• 5519', plan: 'Scale' },
    { id: 'txn_01H8B', invoice: 'INV-2035', customer: 'c10', customerName: 'Elena Vasquez', amount: 49.00, status: 'paid', date: '2026-08-06 10:44', method: 'Visa •• 4242', plan: 'Starter' }
  ];

  var ACTIVITY = [
    { id: 'a1', who: 'Maya Andersson', initials: 'MA', tone: TONES.indigo, userId: 'u2', action: 'upgraded to', target: 'Scale', category: 'subscription', status: 'success', time: '2 min ago', ts: '2026-08-11 16:12' },
    { id: 'a2', who: 'Priya Raman', initials: 'PR', tone: TONES.emerald, userId: 'u3', action: 'paid invoice', target: 'INV-2043 · $240.00', category: 'billing', status: 'success', time: '14 min ago', ts: '2026-08-11 16:00' },
    { id: 'a3', who: 'Jonas Lee', initials: 'JL', tone: TONES.sky, userId: 'u4', action: 'invited 3 members to', target: 'Bright Labs', category: 'team', status: 'info', time: '38 min ago', ts: '2026-08-11 15:36' },
    { id: 'a4', who: 'Diego Costa', initials: 'DC', tone: TONES.amber, userId: 'u6', action: 'started a 14-day trial of', target: 'Growth', category: 'subscription', status: 'info', time: '1 hour ago', ts: '2026-08-11 15:12' },
    { id: 'a5', who: 'Sara Yilmaz', initials: 'SY', tone: TONES.pink, userId: 'u5', action: 'exported the', target: 'Revenue report', category: 'report', status: 'neutral', time: '2 hours ago', ts: '2026-08-11 14:08' },
    { id: 'a6', who: 'Theo Faroe', initials: 'TF', tone: TONES.rose, userId: 'u8', action: 'payment failed for', target: 'INV-2039', category: 'billing', status: 'danger', time: '3 hours ago', ts: '2026-08-11 13:04' },
    { id: 'a7', who: 'Ava Nilsson', initials: 'AN', tone: TONES.teal, userId: 'u7', action: 'added a card on file to', target: 'billing', category: 'billing', status: 'success', time: '5 hours ago', ts: '2026-08-11 11:00' },
    { id: 'a8', who: 'Alex Morgan', initials: 'AM', tone: TONES.indigo, userId: 'u1', action: 'created API key', target: 'Production key', category: 'api', status: 'neutral', time: '6 hours ago', ts: '2026-08-11 10:00' },
    { id: 'a9', who: 'Maya Andersson', initials: 'MA', tone: TONES.indigo, userId: 'u2', action: 'connected', target: 'Slack integration', category: 'integration', status: 'success', time: '8 hours ago', ts: '2026-08-11 08:00' },
    { id: 'a10', who: 'Priya Raman', initials: 'PR', tone: TONES.emerald, userId: 'u3', action: 'updated profile in', target: 'workspace settings', category: 'account', status: 'neutral', time: '12 hours ago', ts: '2026-08-11 04:00' },
    { id: 'a11', who: 'Jonas Lee', initials: 'JL', tone: TONES.sky, userId: 'u4', action: 'changed password', target: '', category: 'security', status: 'warning', time: '1 day ago', ts: '2026-08-10 16:00' },
    { id: 'a12', who: 'Sara Yilmaz', initials: 'SY', tone: TONES.pink, userId: 'u5', action: 'refunded invoice', target: 'INV-2036 · $840.00', category: 'billing', status: 'info', time: '1 day ago', ts: '2026-08-10 14:00' },
    { id: 'a13', who: 'Ava Nilsson', initials: 'AN', tone: TONES.teal, userId: 'u7', action: 'created segment', target: 'High-value accounts', category: 'customer', status: 'neutral', time: '2 days ago', ts: '2026-08-09 11:00' },
    { id: 'a14', who: 'Diego Costa', initials: 'DC', tone: TONES.amber, userId: 'u6', action: 'accepted invitation to', target: 'Summit App', category: 'team', status: 'success', time: '3 days ago', ts: '2026-08-08 09:00' },
    { id: 'a15', who: 'Alex Morgan', initials: 'AM', tone: TONES.indigo, userId: 'u1', action: 'revoked API key', target: 'Staging key', category: 'api', status: 'danger', time: '4 days ago', ts: '2026-08-07 13:00' }
  ];

  var NOTIFICATIONS = [
    { id: 'n1', icon: 'card', tone: TONES.emerald, title: 'Payment received', body: '<strong>Priya Raman</strong> paid invoice INV-2043 ($240.00).', time: '14 min ago', unread: true, category: 'Billing' },
    { id: 'n2', icon: 'user', tone: TONES.sky, title: 'New customer', body: '<strong>Diego Costa</strong> started a 14-day trial of Growth.', time: '1 hour ago', unread: true, category: 'Customers' },
    { id: 'n3', icon: 'alert', tone: TONES.rose, title: 'Payment failed', body: 'Charge for <strong>Theo Faroe</strong> (INV-2039) failed.', time: '3 hours ago', unread: true, category: 'Billing' },
    { id: 'n4', icon: 'team', tone: TONES.violet, title: 'Team member invited', body: '<strong>Jonas Lee</strong> invited 3 members to Bright Labs.', time: '5 hours ago', unread: true, category: 'Team' },
    { id: 'n5', icon: 'analytics', tone: TONES.indigo, title: 'Weekly report ready', body: 'Your revenue summary for last week is available.', time: 'Yesterday', unread: false, category: 'Reports' },
    { id: 'n6', icon: 'key', tone: TONES.amber, title: 'API key created', body: 'A new API key "Production key" was generated.', time: 'Yesterday', unread: false, category: 'API' },
    { id: 'n7', icon: 'integrations', tone: TONES.teal, title: 'Integration connected', body: 'Slack workspace connected by Maya Andersson.', time: '2 days ago', unread: false, category: 'Integrations' },
    { id: 'n8', icon: 'lock', tone: TONES.rose, title: 'Security alert', body: 'New sign-in from an unrecognized device.', time: '3 days ago', unread: false, category: 'Security' }
  ];

  var CONVERSATIONS = [
    { id: 't1', customer: 'c1', name: 'Maya Andersson', company: 'Northwind', initials: 'MA', tone: TONES.indigo, subject: 'Scale plan upgrade question', preview: 'Hi! We are looking to upgrade our team to Scale…', time: '2 min ago', unread: true, priority: 'high', tags: ['billing', 'upgrade'], status: 'open' },
    { id: 't2', customer: 'c7', name: 'Theo Faroe', company: 'Altapine', initials: 'TF', tone: TONES.rose, subject: 'Failed payment — need help', preview: 'My card was declined and I am not sure why…', time: '38 min ago', unread: true, priority: 'urgent', tags: ['billing', 'failed'], status: 'open' },
    { id: 't3', customer: 'c3', name: 'Jonas Lee', company: 'Bright Labs', initials: 'JL', tone: TONES.sky, subject: 'Onboarding help', preview: 'How do I invite my team members to the workspace?', time: '2 hours ago', unread: true, priority: 'normal', tags: ['onboarding'], status: 'open' },
    { id: 't4', customer: 'c6', name: 'Ava Nilsson', company: 'Vantage', initials: 'AN', tone: TONES.teal, subject: 'Invoice receipt request', preview: 'Could you resend the invoice for August?', time: '5 hours ago', unread: true, priority: 'low', tags: ['billing'], status: 'pending' },
    { id: 't5', customer: 'c11', name: 'Marcus Webb', company: 'Vertex', initials: 'MW', tone: TONES.amber, subject: 'Feature comparison', preview: 'How does Northstar compare to your competitor?', time: 'Yesterday', unread: false, priority: 'normal', tags: ['sales'], status: 'open' },
    { id: 't6', customer: 'c10', name: 'Elena Vasquez', company: 'Helix', initials: 'EV', tone: TONES.orange, subject: 'Export to CSV issue', preview: 'The CSV export seems to be missing some columns…', time: 'Yesterday', unread: false, priority: 'normal', tags: ['bug'], status: 'resolved' },
    { id: 't7', customer: 'c4', name: 'Sara Yilmaz', company: 'Altapine', initials: 'SY', tone: TONES.pink, subject: 'Thank you!', preview: 'Just wanted to say the new dashboard is great…', time: '2 days ago', unread: false, priority: 'low', tags: ['feedback'], status: 'resolved' }
  ];

  var CONV_MESSAGES = {
    t1: [
      { who: 'Maya Andersson', initials: 'MA', tone: TONES.indigo, side: 'them', text: 'Hi! We are looking to upgrade our team to the Scale plan. We currently have 12 seats on Growth.', when: '2 min ago' },
      { who: 'Maya Andersson', initials: 'MA', tone: TONES.indigo, side: 'them', text: 'Could you confirm the prorated charge for this billing cycle?', when: '1 min ago' },
      { who: 'You', initials: 'AM', tone: TONES.indigo, side: 'me', text: 'Hi Maya! Happy to help. The prorated charge for 12 seats moving from Growth to Scale would be $7,200 for the remainder of this cycle. Would you like me to process that now?', when: 'just now' }
    ],
    t2: [
      { who: 'Theo Faroe', initials: 'TF', tone: TONES.rose, side: 'them', text: 'My card was declined and I am not sure why. The card is valid and has funds.', when: '38 min ago' },
      { who: 'You', initials: 'AM', tone: TONES.indigo, side: 'me', text: 'Hi Theo, I took a look and it appears the card on file expired last month. You can update it under Billing → Payment methods. Once updated, I can retry the charge for INV-2039 immediately.', when: '30 min ago' }
    ],
    t3: [
      { who: 'Jonas Lee', initials: 'JL', tone: TONES.sky, side: 'them', text: 'How do I invite my team members to the workspace?', when: '2 hours ago' },
      { who: 'You', initials: 'AM', tone: TONES.indigo, side: 'me', text: 'Great question! Go to Workspace → Team, click "Invite members", and enter their email addresses. They will receive an invitation link valid for 7 days.', when: '1 hour ago' }
    ],
    t4: [
      { who: 'Ava Nilsson', initials: 'AN', tone: TONES.teal, side: 'them', text: 'Could you resend the invoice for August?', when: '5 hours ago' },
      { who: 'You', initials: 'AM', tone: TONES.indigo, side: 'me', text: 'Of course! I have just resent INV-2038 to your email. Let me know if you need a copy with different billing details.', when: '4 hours ago' }
    ],
    t5: [
      { who: 'Marcus Webb', initials: 'MW', tone: TONES.amber, side: 'them', text: 'How does Northstar compare to your competitor?', when: 'Yesterday' },
      { who: 'You', initials: 'AM', tone: TONES.indigo, side: 'me', text: 'Great question. Northstar differentiates on three things: our real-time analytics, the built-in customer inbox, and our transparent usage-based pricing. Happy to set up a demo call if that would help.', when: 'Yesterday' }
    ],
    t6: [
      { who: 'Elena Vasquez', initials: 'EV', tone: TONES.orange, side: 'them', text: 'The CSV export seems to be missing some columns — specifically the ARR column.', when: 'Yesterday' },
      { who: 'You', initials: 'AM', tone: TONES.indigo, side: 'me', text: 'Thanks for flagging this, Elena. I have reproduced it and filed a bug. The ARR column will be included in exports again in our next release, scheduled for later this week.', when: 'Yesterday' }
    ],
    t7: [
      { who: 'Sara Yilmaz', initials: 'SY', tone: TONES.pink, side: 'them', text: 'Just wanted to say the new dashboard is great. The activity feed is exactly what we needed.', when: '2 days ago' },
      { who: 'You', initials: 'AM', tone: TONES.indigo, side: 'me', text: 'Thank you so much, Sara! That means a lot. Let us know if there is anything else we can improve.', when: '2 days ago' }
    ]
  };

  var API_KEYS = [
    { id: 'k1', name: 'Production key', prefix: 'ns_live_8f2a', created: '2026-06-12', lastUsed: '2 min ago', scope: 'Full access', status: 'active' },
    { id: 'k2', name: 'Staging key', prefix: 'ns_test_1b9c', created: '2026-05-03', lastUsed: '3 hours ago', scope: 'Read-only', status: 'active' },
    { id: 'k3', name: 'Analytics export', prefix: 'ns_live_4d7e', created: '2026-03-21', lastUsed: '2 days ago', scope: 'Read-only', status: 'active' },
    { id: 'k4', name: 'Legacy webhook', prefix: 'ns_live_9a2f', created: '2025-11-08', lastUsed: '—', scope: 'Webhooks', status: 'expired' }
  ];

  var WEBHOOKS = [
    { id: 'w1', url: 'https://api.northwind.io/hooks/northstar', events: ['invoice.paid', 'customer.created', 'subscription.updated'], status: 'active', lastDelivery: '2 min ago', lastStatus: 'delivered' },
    { id: 'w2', url: 'https://hooks.brightlabs.dev/northstar-events', events: ['invoice.failed'], status: 'active', lastDelivery: '3 hours ago', lastStatus: 'delivered' },
    { id: 'w3', url: 'https://staging.vantage.io/wh/northstar', events: ['customer.created', 'customer.updated'], status: 'inactive', lastDelivery: '2 days ago', lastStatus: 'bounced' }
  ];

  var INTEGRATIONS = [
    { id: 'stripe', name: 'Stripe', desc: 'Accept payments and manage subscriptions through Stripe billing.', connected: true, logo: 'S', tone: TONES.indigo, category: 'Payments' },
    { id: 'slack', name: 'Slack', desc: 'Send notifications and activity alerts to your Slack channels.', connected: true, logo: 'S', tone: TONES.violet, category: 'Communication' },
    { id: 'google', name: 'Google Workspace', desc: 'Sync calendar, import contacts, and enable Google sign-in.', connected: false, logo: 'G', tone: TONES.emerald, category: 'Identity' },
    { id: 'github', name: 'GitHub', desc: 'Link repositories and track deployment activity in your workspace.', connected: false, logo: 'G', tone: TONES.text, category: 'Developer' },
    { id: 'zapier', name: 'Zapier', desc: 'Connect Northstar to 5,000+ apps with automated workflows.', connected: true, logo: 'Z', tone: TONES.orange, category: 'Automation' },
    { id: 'segment', name: 'Segment', desc: 'Stream customer events from Segment into Northstar analytics.', connected: false, logo: 'S', tone: TONES.green || '#22c55e', category: 'Analytics' },
    { id: 'intercom', name: 'Intercom', desc: 'Sync customer conversations between Intercom and Northstar inbox.', connected: false, logo: 'I', tone: TONES.blue, category: 'Support' },
    { id: 'datadog', name: 'Datadog', desc: 'Forward usage metrics and monitor API health via Datadog.', connected: false, logo: 'D', tone: TONES.violet, category: 'Monitoring' }
  ];

  var REPORTS = [
    { id: 'r1', name: 'Revenue summary', category: 'Financial', desc: 'MRR, ARR, and revenue trends by plan.', lastRun: 'Today, 09:00', formats: ['CSV', 'PDF', 'Excel'], schedule: 'Daily', status: 'ready' },
    { id: 'r2', name: 'Customer retention', category: 'Growth', desc: 'Cohort retention and churn analysis.', lastRun: 'Yesterday, 18:00', formats: ['CSV', 'PDF'], schedule: 'Weekly', status: 'ready' },
    { id: 'r3', name: 'Churn analysis', category: 'Growth', desc: 'Detailed breakdown of churned customers and reasons.', lastRun: 'Aug 4, 2026', formats: ['CSV', 'Excel'], schedule: 'Monthly', status: 'ready' },
    { id: 'r4', name: 'Invoice ledger', category: 'Financial', desc: 'Complete invoice history with payment status.', lastRun: 'Today, 06:00', formats: ['CSV', 'PDF', 'Excel'], schedule: 'Daily', status: 'ready' },
    { id: 'r5', name: 'Team activity', category: 'Workspace', desc: 'Audit log of all workspace member actions.', lastRun: '—', formats: ['CSV'], schedule: 'On-demand', status: 'draft' },
    { id: 'r6', name: 'API usage', category: 'Developer', desc: 'API call volume and rate-limit metrics.', lastRun: '2 hours ago', formats: ['CSV', 'PDF'], schedule: 'Daily', status: 'ready' },
    { id: 'r7', name: 'Plan distribution', category: 'Financial', desc: 'Customer count and revenue by subscription plan.', lastRun: 'Yesterday, 12:00', formats: ['CSV', 'PDF', 'Excel'], schedule: 'Weekly', status: 'ready' },
    { id: 'r8', name: 'Conversion funnel', category: 'Growth', desc: 'Trial-to-paid conversion by acquisition source.', lastRun: 'Aug 3, 2026', formats: ['CSV'], schedule: 'Monthly', status: 'scheduled' }
  ];

  var SEGMENTS = [
    { id: 's1', name: 'High-value accounts', desc: 'Scale plan customers with ARR > $10,000', count: 6, color: TONES.indigo, criteria: 'plan = Scale AND arr > 10000' },
    { id: 's2', name: 'Trial users', desc: 'Customers currently on a trial', count: 3, color: TONES.amber, criteria: 'status = trial' },
    { id: 's3', name: 'At-risk', desc: 'Past due or inactive > 7 days', count: 2, color: TONES.rose, criteria: 'status = pastdue OR lastActive > 7d' },
    { id: 's4', name: 'New this month', desc: 'Signed up in the last 30 days', count: 4, color: TONES.emerald, criteria: 'signup within 30d' },
    { id: 's5', name: 'Starter plan', desc: 'All Starter plan customers', count: 3, color: TONES.sky, criteria: 'plan = Starter' }
  ];

  var INVITATIONS = [
    { id: 'i1', email: 'diego@summit.app', name: 'Diego Costa', role: 'Viewer', sent: '2 days ago', status: 'pending', sentBy: 'Alex Morgan' },
    { id: 'i2', email: 'hana@brightlabs.dev', name: 'Hana Kim', role: 'Member', sent: '5 days ago', status: 'pending', sentBy: 'Jonas Lee' },
    { id: 'i3', email: 'omar@cedarworks.co', name: 'Omar Haddad', role: 'Manager', sent: '1 week ago', status: 'expired', sentBy: 'Alex Morgan' },
    { id: 'i4', email: 'clara@fjord.studio', name: 'Clara Berg', role: 'Member', sent: '2 weeks ago', status: 'accepted', sentBy: 'Maya Andersson' }
  ];

  var PAYMENT_METHODS = [
    { id: 'p1', brand: 'Visa', last4: '4242', exp: '08/27', isDefault: true, holder: 'Alex Morgan' },
    { id: 'p2', brand: 'Mastercard', last4: '5519', exp: '11/26', isDefault: false, holder: 'Alex Morgan' },
    { id: 'p3', brand: 'Amex', last4: '1007', exp: '03/28', isDefault: false, holder: 'Maya Andersson' }
  ];

  var PLANS = [
    { name: 'Starter', price: 49, desc: 'For individuals getting started', features: ['1 workspace', 'Up to 3 members', '10k API calls/mo', 'Email support', 'Basic analytics'], current: false, accent: TONES.sky },
    { name: 'Growth', price: 240, desc: 'For growing teams', features: ['5 workspaces', 'Up to 15 members', '250k API calls/mo', 'Priority support', 'Advanced analytics', 'Custom segments', 'API access'], current: false, accent: TONES.emerald, popular: true },
    { name: 'Scale', price: 840, desc: 'For scaling businesses', features: ['Unlimited workspaces', 'Up to 50 members', '1M API calls/mo', '24/7 priority support', 'Real-time analytics', 'Advanced segments', 'Full API access', 'Webhooks', 'Audit logs'], current: true, accent: TONES.indigo },
    { name: 'Enterprise', price: null, desc: 'For large organizations', features: ['Everything in Scale', 'Unlimited members', 'Unlimited API calls', 'Dedicated CSM', 'SSO & SAML', 'Custom contracts', 'On-premise option'], current: false, accent: TONES.violet }
  ];

  var SESSIONS = [
    { id: 'se1', device: 'MacBook Pro · Chrome', location: 'Stockholm, SE', ip: '84.221.x.x', current: true, last: 'Active now' },
    { id: 'se2', device: 'iPhone 15 · Safari', location: 'Stockholm, SE', ip: '84.221.x.x', current: false, last: '2 hours ago' },
    { id: 'se3', device: 'Windows · Firefox', location: 'Oslo, NO', ip: '51.13.x.x', current: false, last: 'Yesterday' },
    { id: 'se4', device: 'iPad · Safari', location: 'Copenhagen, DK', ip: '92.243.x.x', current: false, last: '3 days ago' }
  ];

  var STATUS_COMPONENTS = [
    { name: 'Web application', desc: 'Dashboard and account management', status: 'operational', uptime: '99.98%', history: 'goooogoooogooo' },
    { name: 'API', desc: 'REST and GraphQL endpoints', status: 'operational', uptime: '99.95%', history: 'goooogoooogooo' },
    { name: 'Webhooks delivery', desc: 'Outbound event delivery', status: 'degraded', uptime: '99.21%', history: 'googoogoogogo' },
    { name: 'Billing system', desc: 'Invoicing and payment processing', status: 'operational', uptime: '100.0%', history: 'goooooooooo' },
    { name: 'Analytics pipeline', desc: 'Metrics computation and reporting', status: 'operational', uptime: '99.99%', history: 'goooogoooogoo' },
    { name: 'Email delivery', desc: 'Transactional and notification email', status: 'operational', uptime: '99.92%', history: 'goooogoooogoo' },
    { name: 'File storage', desc: 'Document and asset storage', status: 'operational', uptime: '100.0%', history: 'goooooooooo' }
  ];

  var INCIDENTS = [
    { id: 'inc1', title: 'Webhook delivery delays', date: 'Aug 11, 2026', severity: 'minor', status: 'monitoring', updates: [
      { when: '16:30 UTC', text: 'We are investigating reports of delayed webhook deliveries. Some events may arrive up to 10 minutes late.' },
      { when: '17:15 UTC', text: 'Root cause identified as a backlog in the delivery queue. We are increasing worker capacity.' },
      { when: '18:00 UTC', text: 'Delivery times are returning to normal. We will continue monitoring for the next hour.' }
    ]},
    { id: 'inc2', title: 'Elevated API error rates', date: 'Aug 4, 2026', severity: 'minor', status: 'resolved', updates: [
      { when: '09:20 UTC', text: 'We are investigating an increase in 5xx errors on the API.' },
      { when: '10:05 UTC', text: 'A misconfigured rate limiter was causing the errors. A fix has been deployed.' },
      { when: '10:30 UTC', text: 'Error rates have returned to baseline. The incident is resolved.' }
    ]},
    { id: 'inc3', title: 'Scheduled maintenance', date: 'Jul 28, 2026', severity: 'maintenance', status: 'resolved', updates: [
      { when: '02:00 UTC', text: 'Scheduled maintenance window began. The dashboard may be briefly unavailable.' },
      { when: '02:45 UTC', text: 'Maintenance complete. All systems are operational.' }
    ]}
  ];

  var HELP_ARTICLES = [
    { cat: 'Getting started', items: [
      { title: 'Setting up your workspace', views: '2.4k' },
      { title: 'Inviting your first team members', views: '1.8k' },
      { title: 'Connecting your first integration', views: '1.2k' },
      { title: 'Understanding plans and billing', views: '3.1k' }
    ]},
    { cat: 'Billing', items: [
      { title: 'How to upgrade or downgrade your plan', views: '1.6k' },
      { title: 'Updating your payment method', views: '980' },
      { title: 'Downloading past invoices', views: '1.1k' },
      { title: 'Understanding prorated charges', views: '740' }
    ]},
    { cat: 'Customers', items: [
      { title: 'Creating and managing customer segments', views: '820' },
      { title: 'Importing customers via CSV', views: '1.3k' },
      { title: 'Handling failed payments', views: '610' }
    ]},
    { cat: 'API & webhooks', items: [
      { title: 'Generating your first API key', views: '2.0k' },
      { title: 'Setting up webhook endpoints', views: '1.5k' },
      { title: 'Retry logic for failed deliveries', views: '430' }
    ]}
  ];

  var FAQS = [
    { q: 'How do I change my billing cycle from monthly to annual?', a: 'Go to Billing → Plans, select your plan, and choose the annual billing option. You will receive a prorated credit for the unused portion of your current monthly cycle, and the annual rate (which includes a 2-month discount) takes effect immediately.' },
    { q: 'Can I export all my customer data?', a: 'Yes. Navigate to Customers, click the export button, and choose CSV, PDF, or Excel. The export includes all visible columns and respects any active filters. Large exports are processed in the background and emailed to you when ready.' },
    { q: 'What happens when I hit my API call limit?', a: 'You will receive email notifications at 80%, 90%, and 100% of your quota. Once you reach 100%, API calls return a 429 status. You can upgrade your plan or purchase an API add-on to increase the limit immediately. Usage resets on the first of each billing cycle.' },
    { q: 'How do two-factor authentication and sessions work?', a: 'When 2FA is enabled, sign-in requires your password plus a code from your authenticator app. Active sessions are listed under Settings → Sessions, where you can review devices and revoke any session you do not recognize.' },
    { q: 'Can I customize which notifications I receive?', a: 'Absolutely. Go to Notifications → Preferences (or Settings → Preferences) to toggle email, in-app, and mobile notifications for each category: billing, customers, team, security, reports, and integrations.' },
    { q: 'How do roles and permissions work?', a: 'Northstar has five roles: Owner, Admin, Manager, Member, and Viewer. Each role grants a different level of access across customers, billing, analytics, reports, settings, and team management. You can review the full permissions matrix under Workspace → Roles & permissions.' }
  ];

  var DB = {
    workspace: { name: 'Northstar', plan: 'Scale', owner: 'Alex Morgan', initials: 'AM', ownerEmail: 'alex@northstar.io', billingCycle: 'monthly', nextBillingDate: 'Sep 1, 2026', currentSpend: 840 },
    kpis: {
      mrr: { value: 284920, prefix: '$', delta: 12.4, spark: [248, 252, 251, 258, 263, 269, 271, 278, 281, 285] },
      customers: { value: 12482, delta: 8.1, spark: [11200, 11420, 11610, 11780, 11920, 12010, 12110, 12240, 12360, 12482] },
      conversion: { value: 8.42, suffix: '%', delta: 1.3, deltaDown: true, spark: [8.1, 8.2, 8.05, 8.3, 8.5, 8.4, 8.35, 8.45, 8.4, 8.42] },
      arpu: { value: 22.81, prefix: '$', delta: 3.7, spark: [21.4, 21.6, 21.8, 22.0, 22.1, 22.3, 22.4, 22.5, 22.7, 22.81] }
    },
    revenue: {
      '7d': { labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], current: [38200, 42100, 39800, 47600, 52300, 45100, 54800], previous: [35100, 38900, 37200, 43100, 47600, 41800, 50200] },
      '30d': { labels: ['W1', 'W2', 'W3', 'W4'], current: [248000, 271000, 263000, 285000], previous: [221000, 244000, 239000, 258000] },
      '12m': { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], current: [182000, 196000, 211000, 198000, 224000, 246000, 258000, 251000, 272000, 289000, 312000, 331000], previous: [156000, 168000, 182000, 171000, 194000, 212000, 224000, 218000, 236000, 251000, 272000, 289000] }
    },
    analytics: {
      mrr: 284920, arr: 3419040, activeCustomers: 12482, newCustomers: 348, churnedCustomers: 41, retentionRate: 96.7, churnRate: 3.3, conversionRate: 8.42, arrDelta: 14.2, newDelta: 22.1, churnDelta: -8.2, retentionDelta: 1.4,
      mrrTrend: [248, 252, 251, 258, 263, 269, 271, 278, 281, 285, 284, 285],
      newCustomersTrend: [280, 310, 295, 340, 325, 360, 348, 355, 370, 342, 360, 348],
      churnTrend: [52, 48, 45, 50, 44, 42, 39, 43, 41, 38, 40, 41],
      traffic: { labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], visitors: [4200, 4800, 5100, 5600, 6200, 3800, 4100], signups: [312, 348, 401, 422, 510, 280, 305] },
      sources: [ { name: 'Organic search', value: 38, color: TONES.indigo }, { name: 'Direct', value: 24, color: TONES.sky }, { name: 'Referral', value: 18, color: TONES.emerald }, { name: 'Social', value: 12, color: TONES.amber }, { name: 'Paid', value: 8, color: TONES.rose } ],
      engagement: { labels: ['W1','W2','W3','W4'], dau: [8200, 8800, 9100, 9600], mau: [11200, 11420, 11610, 12482] },
      sessions: { avgDuration: '4m 12s', avgPages: 6.4, bounceRate: 38.2, dau: 9600 }
    },
    plans: PLANS,
    activity: ACTIVITY,
    transactions: TRANSACTIONS,
    invoices: INVOICES,
    customers: CUSTOMERS,
    team: TEAM,
    notifications: NOTIFICATIONS,
    conversations: CONVERSATIONS,
    convMessages: CONV_MESSAGES,
    apiKeys: API_KEYS,
    webhooks: WEBHOOKS,
    integrations: INTEGRATIONS,
    reports: REPORTS,
    segments: SEGMENTS,
    invitations: INVITATIONS,
    paymentMethods: PAYMENT_METHODS,
    sessions: SESSIONS,
    statusComponents: STATUS_COMPONENTS,
    incidents: INCIDENTS,
    helpArticles: HELP_ARTICLES,
    faqs: FAQS,
    usage: { seats: 18, seatsMax: 25, apiCalls: 482300, apiMax: 1000000, storage: 184, storageMax: 500 }
  };
  window.DB = DB;
  window.ICONS = ICONS;
  window.NAV = NAV;
  window.SETTINGS_NAV = SETTINGS_NAV;
  window.TONES = TONES;

  /* =====================================================================
     HELPERS
  ===================================================================== */
  function fmt(n, prefix, suffix, decimals) {
    var d = decimals == null ? (n % 1 === 0 ? 0 : 2) : decimals;
    var s = n.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
    return (prefix || '') + s + (suffix || '');
  }
  function compact(n) {
    if (n >= 1000000) return (n / 1000000).toFixed(n % 1000000 === 0 ? 0 : 1) + 'M';
    if (n >= 1000) return (n / 1000).toFixed(n % 1000 === 0 ? 0 : 1) + 'k';
    return String(Math.round(n));
  }
  function money(n) { return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 }); }
  function money2(n) { return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function cssVar(name) { return getComputedStyle(root).getPropertyValue(name).trim(); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function pill(status) { return '<span class="pill ' + esc(status) + '">' + esc(statusLabel(status)) + '</span>'; }
  function statusLabel(s) {
    var map = { active: 'Active', trial: 'Trial', trialing: 'Trialing', pastdue: 'Past due', paid: 'Paid', pending: 'Pending', failed: 'Failed', refunded: 'Refunded', overdue: 'Overdue', invited: 'Invited', suspended: 'Suspended', expired: 'Expired', accepted: 'Accepted', operational: 'Operational', degraded: 'Degraded', connected: 'Connected', disconnected: 'Disconnected', delivered: 'Delivered', bounced: 'Bounced', scheduled: 'Scheduled', draft: 'Draft', ready: 'Ready', open: 'Open', resolved: 'Resolved' };
    return map[s] || s;
  }
  function avatar(initials, tone, size) { size = size || ''; return '<span class="avatar-pic ' + size + '" style="background:' + tone + '">' + initials + '</span>'; }
  function deltaHtml(delta, down) {
    var cls = down ? 'down' : 'up', ic = down ? ICONS.arrowDown : ICONS.arrowUp;
    return '<span class="delta ' + cls + '">' + ic + ' ' + Math.abs(delta).toFixed(1) + '% <span class="vs">vs last period</span></span>';
  }

  window.NS = {
    fmt: fmt, compact: compact, money: money, money2: money2, cssVar: cssVar, esc: esc,
    pill: pill, statusLabel: statusLabel, avatar: avatar, deltaHtml: deltaHtml, ICONS: ICONS, DB: DB, TONES: TONES
  };

  /* =====================================================================
     APP SHELL — renders sidebar + topbar around <main data-page>.
     Each page provides: <main class="main" data-page="dashboard">…</main>
     and sets <body data-page="dashboard">. app.js injects the shell.
  ===================================================================== */
  function currentPage() {
    var path = location.pathname.split('/').pop() || 'dashboard.html';
    return path.replace('.html', '');
  }

  function buildSidebar() {
    var page = currentPage();
    var groups = NAV.map(function (g) {
      var items = g.items.map(function (it) {
        var active = it.id === page ? ' aria-current="page"' : '';
        var count = it.count != null ? ' <span class="count">' + it.count + '</span>' : '';
        return '<a href="' + it.href + '"' + active + '>' + (ICONS[it.icon] || ICONS.dashboard) + ' ' + esc(it.label) + count + '</a>';
      }).join('');
      return '<div class="nav-group"><div class="nav-label">' + esc(g.group) + '</div>' + items + '</div>';
    }).join('');
    return '<aside class="sidebar" id="sidebar" aria-label="Primary">' +
      '<div class="brand"><span class="mark">N</span><div><div class="name">' + esc(DB.workspace.name) + '</div><div class="plan-tag">' + esc(DB.workspace.plan) + ' · Workspace</div></div></div>' +
      '<nav class="nav">' + groups + '</nav>' +
      '<div class="side-foot"><span class="pic">' + DB.workspace.initials + '</span><div class="who"><div class="nm">' + esc(DB.workspace.owner) + '</div><div class="rl">Workspace owner</div></div><a class="gear" href="profile.html" aria-label="Account settings">' + ICONS.chevronRight + '</a></div>' +
    '</aside>';
  }

  function buildTopbar() {
    var unread = DB.notifications.filter(function (n) { return n.unread; }).length;
    return '<header class="topbar">' +
      '<button class="menu-btn" aria-label="Toggle navigation" aria-expanded="false" aria-controls="sidebar">' + ICONS.menu + '</button>' +
      '<div class="search">' + ICONS.search + '<input type="search" placeholder="Search customers, invoices, reports…" aria-label="Search"><span class="kbd">⌘K</span></div>' +
      '<div class="header-actions">' +
        '<div style="position:relative">' +
          '<button class="icon-btn" id="notif-btn" aria-label="Notifications" aria-haspopup="true" aria-expanded="false">' + (unread ? '<span class="count-badge">' + unread + '</span>' : '<span class="badge"></span>') + ICONS.notifications + '</button>' +
          buildNotifDropdown(unread) +
        '</div>' +
        '<button class="icon-btn theme-toggle" aria-label="Toggle dark mode" aria-pressed="false">' + '<svg class="moon">' + ICONS.moon + '</svg>' + '<svg class="sun">' + ICONS.sun + '</svg>' + '</button>' +
        '<a class="acct" href="profile.html" aria-label="Account"><span class="pic">' + DB.workspace.initials + '</span><span class="nm">Alex</span>' + ICONS.chevronDown + '</a>' +
      '</div>' +
    '</header>';
  }

  function buildNotifDropdown(unread) {
    var list = DB.notifications.slice(0, 5).map(function (n) {
      return '<li class="' + (n.unread ? 'unread' : '') + '">' +
        '<span class="ic" style="background:' + n.tone + '">' + (ICONS[n.icon] || ICONS.bell) + '</span>' +
        '<div class="body"><p class="txt">' + n.body + '</p><p class="when">' + n.time + '</p></div></li>';
    }).join('');
    return '<div class="notif-dropdown" id="notif-dropdown" role="menu" aria-label="Notifications">' +
      '<div class="notif-head"><h3>Notifications</h3>' + (unread ? '<a href="notifications.html" id="mark-all-read">' + unread + ' unread</a>' : '') + '</div>' +
      '<ul class="notif-list">' + list + '</ul>' +
      '<div class="notif-foot"><a href="notifications.html">View all notifications</a></div></div>';
  }

  function injectShell() {
    var main = document.querySelector('main[data-page]');
    if (!main) return;
    var content = document.createElement('div');
    content.className = 'content';
    main.parentNode.insertBefore(content, main);
    content.appendChild(main);

    var sidebar = document.createElement('div');
    sidebar.innerHTML = buildSidebar();
    content.parentNode.insertBefore(sidebar.firstChild, content);

    var topbar = document.createElement('div');
    topbar.innerHTML = buildTopbar();
    content.insertBefore(topbar.firstChild, main);

    var backdrop = document.createElement('div');
    backdrop.className = 'backdrop';
    backdrop.setAttribute('tabindex', '-1');
    backdrop.setAttribute('aria-hidden', 'true');
    content.parentNode.appendChild(backdrop);
  }

  /* =====================================================================
     THEME
  ===================================================================== */
  function applyTheme(dark) {
    root.dataset.theme = dark ? 'dark' : 'light';
    var t = document.querySelector('.theme-toggle');
    if (t) t.setAttribute('aria-pressed', String(dark));
    try { localStorage.setItem('ns-theme', dark ? 'dark' : 'light'); } catch (e) {}
    window.dispatchEvent(new CustomEvent('ns:theme', { detail: { dark: dark } }));
  }
  function storedTheme() {
    try { var v = localStorage.getItem('ns-theme'); if (v) return v === 'dark'; } catch (e) {}
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  /* =====================================================================
     SIDEBAR (mobile drawer)
  ===================================================================== */
  function wireSidebar() {
    var app = document.querySelector('.app') || document.querySelector('.content');
    if (!app) return;
    var menuBtn = document.querySelector('.menu-btn');
    function closeSidebar() { document.body.classList.remove('sidebar-open'); if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false'); }
    if (menuBtn) {
      menuBtn.addEventListener('click', function () {
        var open = document.body.classList.toggle('sidebar-open');
        menuBtn.setAttribute('aria-expanded', String(open));
      });
    }
    var backdrop = document.querySelector('.backdrop');
    if (backdrop) backdrop.addEventListener('click', closeSidebar);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('sidebar-open')) closeSidebar();
    });
  }

  /* =====================================================================
     NOTIFICATIONS DROPDOWN
  ===================================================================== */
  function wireNotifications() {
    var btn = document.getElementById('notif-btn');
    var dd = document.getElementById('notif-dropdown');
    if (!btn || !dd) return;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = dd.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', function (e) {
      if (!dd.contains(e.target) && e.target !== btn) {
        dd.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
    var markAll = document.getElementById('mark-all-read');
    if (markAll) markAll.addEventListener('click', function (e) {
      e.preventDefault();
      DB.notifications.forEach(function (n) { n.unread = false; });
      var badge = btn.querySelector('.count-badge, .badge');
      if (badge) badge.remove();
      dd.querySelectorAll('.unread').forEach(function (li) { li.classList.remove('unread'); });
      var head = dd.querySelector('.notif-head');
      var link = head.querySelector('a');
      if (link) link.remove();
      showToast('All notifications marked as read', 'success');
    });
  }

  /* =====================================================================
     TOAST
  ===================================================================== */
  function ensureToast() {
    var t = document.getElementById('toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'toast';
      t.setAttribute('role', 'status');
      t.setAttribute('aria-live', 'polite');
      document.body.appendChild(t);
    }
    return t;
  }
  function showToast(msg, kind) {
    var t = ensureToast();
    var ic = kind === 'success' ? ICONS.checkCircle : kind === 'danger' ? ICONS.xCircle : ICONS.info;
    t.className = kind || '';
    t.innerHTML = '<span class="ic">' + ic + '</span>' + esc(msg);
    t.classList.add('show');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(function () { t.classList.remove('show'); }, 2600);
  }

  /* =====================================================================
     MODAL / DRAWER / CONFIRM  (programmatic)
  ===================================================================== */
  function openModal(opts) {
    closeOverlay();
    var bd = document.createElement('div');
    bd.className = 'modal-backdrop';
    bd.innerHTML = '<div class="modal ' + (opts.size || '') + '" role="dialog" aria-modal="true" aria-labelledby="m-title">' +
      '<div class="modal-head"><div class="titles"><h2 id="m-title">' + esc(opts.title || '') + '</h2>' + (opts.sub ? '<p class="sub">' + esc(opts.sub) + '</p>' : '') + '</div><button class="modal-close" aria-label="Close">' + ICONS.close + '</button></div>' +
      '<div class="modal-body">' + (opts.body || '') + '</div>' +
      (opts.foot != null ? '<div class="modal-foot">' + opts.foot + '</div>' : '') +
    '</div>';
    document.body.appendChild(bd);
    requestAnimationFrame(function () { bd.classList.add('is-open'); });
    function close() { bd.classList.remove('is-open'); setTimeout(function () { bd.remove(); }, 180); }
    bd.querySelector('.modal-close').addEventListener('click', close);
    bd.addEventListener('click', function (e) { if (e.target === bd) close(); });
    document.addEventListener('keydown', function esc(e) { if (e.key === 'Escape') { close(); document.removeEventListener('keydown', esc); } });
    if (opts.onOpen) opts.onOpen(bd, close);
    return { close: close, el: bd };
  }
  function openDrawer(opts) {
    closeOverlay();
    var bd = document.createElement('div');
    bd.className = 'drawer-backdrop';
    var dw = document.createElement('div');
    dw.className = 'drawer';
    dw.setAttribute('role', 'dialog');
    dw.setAttribute('aria-modal', 'true');
    dw.innerHTML = '<div class="drawer-head"><h2>' + esc(opts.title || '') + '</h2><button class="modal-close" aria-label="Close">' + ICONS.close + '</button></div>' +
      '<div class="drawer-body">' + (opts.body || '') + '</div>' +
      (opts.foot != null ? '<div class="drawer-foot">' + opts.foot + '</div>' : '');
    document.body.appendChild(bd, dw);
    document.body.appendChild(dw);
    requestAnimationFrame(function () { bd.classList.add('is-open'); dw.classList.add('is-open'); });
    function close() { bd.classList.remove('is-open'); dw.classList.remove('is-open'); setTimeout(function () { bd.remove(); dw.remove(); }, 220); }
    dw.querySelector('.modal-close').addEventListener('click', close);
    bd.addEventListener('click', close);
    document.addEventListener('keydown', function esc(e) { if (e.key === 'Escape') { close(); document.removeEventListener('keydown', esc); } });
    if (opts.onOpen) opts.onOpen(dw, close);
    return { close: close, el: dw };
  }
  function confirmDialog(opts) {
    var ic = opts.danger ? '<span class="ic danger">' + ICONS.alert + '</span>' : '<span class="ic accent">' + ICONS.info + '</span>';
    openModal({
      title: opts.title || 'Confirm',
      size: 'sm',
      body: '<div class="state" style="padding:8px 0;text-align:left;align-items:flex-start"><div style="display:flex;gap:14px;align-items:flex-start">' + ic + '<div><p style="font-size:14px;color:var(--ds-text);margin:0">' + esc(opts.message) + '</p>' + (opts.hint ? '<p class="muted-block" style="margin-top:8px">' + esc(opts.hint) + '</p>' : '') + '</div></div></div>',
      foot: '<button class="btn" data-cancel>Cancel</button><button class="btn ' + (opts.danger ? 'btn-danger' : 'btn-primary') + '" data-confirm>' + esc(opts.confirmLabel || 'Confirm') + '</button>',
      onOpen: function (bd, close) {
        bd.querySelector('[data-cancel]').addEventListener('click', close);
        bd.querySelector('[data-confirm]').addEventListener('click', function () { close(); if (opts.onConfirm) opts.onConfirm(); });
      }
    });
  }
  function closeOverlay() {
    document.querySelectorAll('.modal-backdrop.is-open, .drawer-backdrop.is-open').forEach(function (el) { el.classList.remove('is-open'); });
    document.querySelectorAll('.drawer.is-open').forEach(function (el) { el.classList.remove('is-open'); });
    setTimeout(function () {
      document.querySelectorAll('.modal-backdrop').forEach(function (el) { if (!el.classList.contains('is-open')) el.remove(); });
      document.querySelectorAll('.drawer-backdrop, .drawer').forEach(function (el) { if (!el.classList.contains('is-open')) el.remove(); });
    }, 230);
  }

  /* =====================================================================
     TABS (data-tabs container with [role=tab] buttons + .tab-panel)
  ===================================================================== */
  function wireTabs(scope) {
    (scope || document).querySelectorAll('[data-tabs]').forEach(function (tabs) {
      var btns = tabs.querySelectorAll('[role="tab"]');
      btns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          btns.forEach(function (b) { b.setAttribute('aria-selected', 'false'); });
          btn.setAttribute('aria-selected', 'true');
          var target = btn.getAttribute('data-tab');
          var panels = tabs.querySelectorAll('.tab-panel');
          panels.forEach(function (p) { p.classList.toggle('is-active', p.getAttribute('data-panel') === target); });
          if (tabs.dataset.onTab) { var fn = window[tabs.dataset.onTab]; if (fn) fn(target); }
        });
      });
    });
  }

  /* =====================================================================
     FAQ accordion + generic [data-accordion]
  ===================================================================== */
  function wireAccordions(scope) {
    (scope || document).querySelectorAll('.faq-item').forEach(function (item) {
      var q = item.querySelector('.faq-q');
      if (q) q.addEventListener('click', function () { item.classList.toggle('is-open'); q.setAttribute('aria-expanded', String(item.classList.contains('is-open'))); });
    });
    (scope || document).querySelectorAll('[data-accordion]').forEach(function (host) {
      host.addEventListener('click', function (e) {
        var head = e.target.closest('[data-acc-head]');
        if (!head) return;
        var item = head.closest('[data-acc-item]');
        if (item) item.classList.toggle('is-open');
      });
    });
  }

  /* =====================================================================
     THEME TOGGLE + global wiring
  ===================================================================== */
  function wireThemeToggle() {
    var t = document.querySelector('.theme-toggle');
    if (t) t.addEventListener('click', function () { applyTheme(root.dataset.theme !== 'dark'); });
  }

  /* =====================================================================
     CHART UTILITIES
  ===================================================================== */
  function sparkPath(values, w, h, pad) {
    pad = pad || 2;
    var min = Math.min.apply(null, values);
    var max = Math.max.apply(null, values);
    var span = Math.max(1e-9, max - min);
    var stepX = (w - pad * 2) / Math.max(1, values.length - 1);
    return values.map(function (v, i) {
      return (i === 0 ? 'M' : 'L') + (pad + i * stepX).toFixed(1) + ' ' + (h - pad - ((v - min) / span) * (h - pad * 2)).toFixed(1);
    }).join(' ');
  }
  function renderSparklines() {
    var success = cssVar('--ds-success') || '#10b981';
    var danger = cssVar('--ds-danger') || '#ef4444';
    document.querySelectorAll('[data-spark]').forEach(function (el) {
      var key = el.dataset.spark;
      var k = DB.kpis[key] || DB.analytics[key];
      if (!k || !k.spark) {
        var arr = el.dataset.values ? el.dataset.values.split(',').map(Number) : null;
        if (!arr) return;
        k = { spark: arr, deltaDown: el.dataset.down === 'true' };
      }
      var w = 120, h = 36;
      var line = sparkPath(k.spark, w, h, 3);
      var area = line + ' L ' + (w - 3) + ' ' + h + ' L 3 ' + h + ' Z';
      var col = k.deltaDown ? danger : success;
      var gid = 'sp-' + key + '-' + Math.random().toString(36).slice(2, 7);
      el.innerHTML =
        '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" role="img" aria-label="' + key + ' trend">' +
        '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="' + col + '" stop-opacity="0.22"/>' +
        '<stop offset="1" stop-color="' + col + '" stop-opacity="0"/>' +
        '</linearGradient></defs>' +
        '<path d="' + area + '" fill="url(#' + gid + ')"/>' +
        '<path d="' + line + '" fill="none" stroke="' + col + '" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
        '</svg>';
    });
  }
  window.renderSparklines = renderSparklines;

  function niceBounds(min, max) {
    var range = max - min || max || 1;
    var raw = range * 0.15;
    var mag = Math.pow(10, Math.floor(Math.log10(raw)));
    var nice = Math.ceil(raw / mag) * mag;
    return { lo: Math.max(0, min - nice), hi: max + nice };
  }
  function fmtAxis(n) { return n >= 1000 ? '$' + compact(n) : '$' + Math.round(n); }

  function drawLineChart(svg, data, opts) {
    opts = opts || {};
    var W = 980, H = 320;
    var mL = 52, mR = 16, mT = opts.mT || 16, mB = 34;
    var innerW = W - mL - mR, innerH = H - mT - mB;
    var n = data.labels.length;
    var all = data.current.concat(data.previous || []);
    var b = niceBounds(Math.min.apply(null, all), Math.max.apply(null, all));
    var stepX = innerW / Math.max(1, n - 1);
    function toPts(arr) { return arr.map(function (v, i) { return { x: mL + i * stepX, y: mT + (1 - (v - b.lo) / (b.hi - b.lo)) * innerH, v: v }; }); }
    var cur = toPts(data.current);
    var prev = data.previous ? toPts(data.previous) : null;
    function lineOf(pts) { return pts.map(function (p, i) { return (i === 0 ? 'M' : 'L') + p.x.toFixed(1) + ' ' + p.y.toFixed(1); }).join(' '); }
    var curLine = lineOf(cur);
    var curArea = curLine + ' L ' + cur[cur.length - 1].x.toFixed(1) + ' ' + (mT + innerH) + ' L ' + cur[0].x.toFixed(1) + ' ' + (mT + innerH) + ' Z';
    var grid = '';
    for (var g = 0; g <= 4; g++) {
      var gy = mT + (g / 4) * innerH;
      var gv = b.hi - (g / 4) * (b.hi - b.lo);
      grid += '<line x1="' + mL + '" y1="' + gy.toFixed(1) + '" x2="' + (W - mR) + '" y2="' + gy.toFixed(1) + '" class="g-grid"/>';
      grid += '<text x="' + (mL - 10) + '" y="' + (gy + 3.5).toFixed(1) + '" text-anchor="end" class="g-axis">' + (opts.axisFmt ? opts.axisFmt(gv) : fmtAxis(gv)) + '</text>';
    }
    var xlabels = data.labels.map(function (l, i) { return '<text x="' + cur[i].x.toFixed(1) + '" y="' + (H - 12) + '" text-anchor="middle" class="g-axis">' + l + '</text>'; }).join('');
    var accent = cssVar('--ds-accent') || '#4f46e5';
    var faint = cssVar('--ds-faint') || '#94a3b8';
    var gid = 'area-' + Math.random().toString(36).slice(2, 7);
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.innerHTML =
      '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + accent + '" stop-opacity="0.18"/><stop offset="1" stop-color="' + accent + '" stop-opacity="0"/></linearGradient></defs>' +
      grid +
      (prev ? '<path d="' + lineOf(prev) + '" fill="none" stroke="' + faint + '" stroke-width="1.5" stroke-dasharray="4 4" class="g-prev" opacity="0.7"/>' : '') +
      '<path d="' + curArea + '" fill="url(#' + gid + ')"/>' +
      '<path d="' + curLine + '" fill="none" stroke="' + accent + '" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="g-line"/>' +
      cur.map(function (p) { return '<circle cx="' + p.x.toFixed(1) + '" cy="' + p.y.toFixed(1) + '" r="3.2" class="g-pt"/>'; }).join('') +
      xlabels +
      '<line id="hair" x1="0" y1="' + mT + '" x2="0" y2="' + (mT + innerH) + '" class="g-hair" opacity="0"/>' +
      '<g id="tip" opacity="0"><rect x="0" y="0" width="150" height="58" rx="8" class="g-tip-bg"/><text id="tip-label" x="12" y="20" class="g-tip-label"></text><text id="tip-cur" x="12" y="40" class="g-tip-cur"></text><text id="tip-prev" x="12" y="54" class="g-tip-prev"></text></g>' +
      '<rect id="overlay" x="0" y="0" width="' + W + '" height="' + H + '" fill="transparent"/>';
    wireLineTooltip(svg, cur, data.labels, data.current, data.previous || [], mL, W, opts.valueFmt);
  }
  function wireLineTooltip(svg, cur, labels, curVals, prevVals, mL, W, valueFmt) {
    var overlay = svg.querySelector('#overlay');
    var hair = svg.querySelector('#hair');
    var tip = svg.querySelector('#tip');
    var tipLabel = svg.querySelector('#tip-label');
    var tipCur = svg.querySelector('#tip-cur');
    var tipPrev = svg.querySelector('#tip-prev');
    if (!overlay) return;
    var mR = 16, innerW = W - mL - mR;
    var stepX = innerW / Math.max(1, cur.length - 1);
    var vf = valueFmt || money;
    function move(clientX) {
      var rect = svg.getBoundingClientRect();
      var relX = ((clientX - rect.left) / rect.width) * W;
      var i = Math.round((relX - mL) / stepX);
      i = Math.max(0, Math.min(cur.length - 1, i));
      var p = cur[i];
      hair.setAttribute('x1', p.x); hair.setAttribute('x2', p.x); hair.setAttribute('opacity', '1');
      var tx = Math.min(W - 160, Math.max(8, p.x - 75));
      tip.setAttribute('transform', 'translate(' + tx + ',' + (p.y - 70) + ')');
      tip.setAttribute('opacity', '1');
      tipLabel.textContent = labels[i];
      tipCur.textContent = 'This period  ' + vf(curVals[i]);
      tipPrev.textContent = prevVals.length ? 'Last period  ' + vf(prevVals[i]) : '';
    }
    overlay.addEventListener('mousemove', function (e) { move(e.clientX); });
    overlay.addEventListener('mouseleave', function () { hair.setAttribute('opacity', '0'); tip.setAttribute('opacity', '0'); });
    overlay.addEventListener('touchmove', function (e) { if (e.touches[0]) move(e.touches[0].clientX); }, { passive: true });
  }

  function drawBarChart(svg, data, opts) {
    opts = opts || {};
    var W = 980, H = 280;
    var mL = 52, mR = 16, mT = 16, mB = 34;
    var innerW = W - mL - mR, innerH = H - mT - mB;
    var n = data.labels.length;
    var max = Math.max.apply(null, data.current.concat(data.previous || [0]));
    var b = niceBounds(0, max);
    var gap = 0.3;
    var barW = innerW / n * (1 - gap);
    var groupW = innerW / n;
    var accent = cssVar('--ds-accent') || '#4f46e5';
    var accent2 = cssVar('--ds-info') || '#0ea5e9';
    var grid = '';
    for (var g = 0; g <= 4; g++) {
      var gy = mT + (g / 4) * innerH;
      var gv = b.hi - (g / 4) * (b.hi - b.lo);
      grid += '<line x1="' + mL + '" y1="' + gy.toFixed(1) + '" x2="' + (W - mR) + '" y2="' + gy.toFixed(1) + '" class="g-grid"/>';
      grid += '<text x="' + (mL - 10) + '" y="' + (gy + 3.5).toFixed(1) + '" text-anchor="end" class="g-axis">' + (opts.axisFmt ? opts.axisFmt(gv) : compact(gv)) + '</text>';
    }
    var bars = '';
    data.labels.forEach(function (l, i) {
      var x = mL + i * groupW + groupW * gap / 2;
      if (data.previous) {
        var pv = data.previous[i];
        var ph = ((pv - b.lo) / (b.hi - b.lo)) * innerH;
        bars += '<rect class="g-bar" x="' + x.toFixed(1) + '" y="' + (mT + innerH - ph).toFixed(1) + '" width="' + (barW / 2 - 2).toFixed(1) + '" height="' + ph.toFixed(1) + '" fill="' + accent2 + '" rx="2"><title>' + l + ' (last): ' + (opts.valueFmt ? opts.valueFmt(pv) : pv) + '</title></rect>';
        var cv = data.current[i];
        var ch = ((cv - b.lo) / (b.hi - b.lo)) * innerH;
        bars += '<rect class="g-bar" x="' + (x + barW / 2 + 2).toFixed(1) + '" y="' + (mT + innerH - ch).toFixed(1) + '" width="' + (barW / 2 - 2).toFixed(1) + '" height="' + ch.toFixed(1) + '" fill="' + accent + '" rx="2"><title>' + l + ': ' + (opts.valueFmt ? opts.valueFmt(cv) : cv) + '</title></rect>';
      } else {
        var v = data.current[i];
        var h = ((v - b.lo) / (b.hi - b.lo)) * innerH;
        bars += '<rect class="g-bar" x="' + x.toFixed(1) + '" y="' + (mT + innerH - h).toFixed(1) + '" width="' + barW.toFixed(1) + '" height="' + h.toFixed(1) + '" fill="' + accent + '" rx="2"><title>' + l + ': ' + (opts.valueFmt ? opts.valueFmt(v) : v) + '</title></rect>';
      }
      bars += '<text x="' + (x + barW / 2).toFixed(1) + '" y="' + (H - 12) + '" text-anchor="middle" class="g-axis">' + l + '</text>';
    });
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.innerHTML = grid + bars;
  }

  function drawDonut(svg, data) {
    var size = 220, cx = size / 2, cy = size / 2, r = 80, sw = 22;
    var total = data.reduce(function (s, d) { return s + d.value; }, 0);
    var circ = 2 * Math.PI * r;
    var offset = 0;
    var segs = data.map(function (d) {
      var frac = d.value / total;
      var len = frac * circ;
      var seg = '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="none" stroke="' + d.color + '" stroke-width="' + sw + '" stroke-dasharray="' + len.toFixed(2) + ' ' + (circ - len).toFixed(2) + '" stroke-dashoffset="' + (-offset).toFixed(2) + '" transform="rotate(-90 ' + cx + ' ' + cy + ')" stroke-linecap="butt"><title>' + d.name + ': ' + Math.round(frac * 100) + '%</title></circle>';
      offset += len;
      return seg;
    }).join('');
    svg.setAttribute('viewBox', '0 0 ' + size + ' ' + size);
    svg.classList.add('donut');
    svg.innerHTML = '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="none" stroke="' + (cssVar('--ds-sunken') || '#f1f3f6') + '" stroke-width="' + sw + '"/>' + segs +
      '<text x="' + cx + '" y="' + (cy - 2) + '" text-anchor="middle" class="donut-center">' + (data.length ? compact(total) : '0') + '</text>' +
      '<text x="' + cx + '" y="' + (cy + 16) + '" text-anchor="middle" class="donut-center-sub">TOTAL</text>';
  }

  window.NSCharts = { sparkPath: sparkPath, drawLineChart: drawLineChart, drawBarChart: drawBarChart, drawDonut: drawDonut, renderSparklines: renderSparklines, fmtAxis: fmtAxis, niceBounds: niceBounds };

  /* =====================================================================
     SHARED TABLE HELPERS (pagination rendering)
  ===================================================================== */
  function renderPagination(host, state, total, onChange) {
    var pages = Math.max(1, Math.ceil(total / state.perPage));
    if (state.page > pages) state.page = 1;
    var btns = '';
    btns += '<button class="page" data-page="' + (state.page - 1) + '"' + (state.page === 1 ? ' disabled' : '') + ' aria-label="Previous page">‹</button>';
    var from = Math.max(1, state.page - 2), to = Math.min(pages, from + 4);
    if (from > 1) { btns += '<button class="page" data-page="1">1</button>'; if (from > 2) btns += '<span class="page" style="border:none;background:none">…</span>'; }
    for (var i = from; i <= to; i++) { btns += '<button class="page' + (i === state.page ? ' is-current' : '') + '" data-page="' + i + '"' + (i === state.page ? ' aria-current="page"' : '') + '>' + i + '</button>'; }
    if (to < pages) { if (to < pages - 1) btns += '<span class="page" style="border:none;background:none">…</span>'; btns += '<button class="page" data-page="' + pages + '">' + pages + '</button>'; }
    btns += '<button class="page" data-page="' + (state.page + 1) + '"' + (state.page === pages ? ' disabled' : '') + ' aria-label="Next page">›</button>';
    var s = (state.page - 1) * state.perPage + 1, e = Math.min(total, state.page * state.perPage);
    host.innerHTML = '<span class="page-info">Showing ' + (total === 0 ? 0 : s) + '–' + e + ' of ' + total + '</span><div class="page-btns">' + btns + '</div>';
    host.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-page]:not(:disabled)');
      if (!b) return;
      var p = parseInt(b.dataset.page, 10);
      if (p >= 1 && p <= pages && p !== state.page) { state.page = p; onChange(); }
    });
  }
  window.NS.renderPagination = renderPagination;

  /* =====================================================================
     COUNT-UP
  ===================================================================== */
  function animateNumber(el) {
    var target = parseFloat(el.dataset.value);
    var prefix = el.dataset.prefix || '';
    var suffix = el.dataset.suffix || '';
    var dec = parseInt(el.dataset.decimals || '0', 10);
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) { el.textContent = fmt(target, prefix, suffix, dec); return; }
    var start = null, dur = 800;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(target * eased, prefix, suffix, dec);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* =====================================================================
     GLOBAL CLICK HANDLERS (toast buttons, copy, confirm-delete)
  ===================================================================== */
  function wireGlobalActions() {
    document.addEventListener('click', function (e) {
      var toastBtn = e.target.closest('[data-toast]');
      if (toastBtn) { showToast(toastBtn.dataset.toast); return; }
      var copyBtn = e.target.closest('[data-copy]');
      if (copyBtn) {
        var txt = copyBtn.dataset.copy;
        if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { showToast('Copied to clipboard', 'success'); });
        else { showToast('Copied to clipboard', 'success'); }
        return;
      }
      var confirmBtn = e.target.closest('[data-confirm]');
      if (confirmBtn) {
        e.preventDefault();
        confirmDialog({
          title: confirmBtn.dataset.confirmTitle || 'Are you sure?',
          message: confirmBtn.dataset.confirm || 'This action cannot be undone.',
          hint: confirmBtn.dataset.hint || '',
          danger: confirmBtn.dataset.danger === 'true',
          confirmLabel: confirmBtn.dataset.confirmLabel || 'Confirm',
          onConfirm: function () {
            if (confirmBtn.dataset.confirmed) { var fn = window[confirmBtn.dataset.confirmed]; if (fn) fn(confirmBtn); }
            else showToast('Action completed', 'success');
          }
        });
        return;
      }
    });
    document.addEventListener('input', function (e) {
      var filter = e.target.closest('[data-filter-target]');
      if (filter) { var fn = window[filter.dataset.filterTarget]; if (fn) fn(filter.value); }
    });
  }

  /* =====================================================================
     SETTINGS NAV (for settings pages using .settings-nav)
  ===================================================================== */
  function buildSettingsNav() {
    var host = document.querySelector('[data-settings-nav]');
    if (!host) return;
    var page = currentPage();
    host.innerHTML = SETTINGS_NAV.map(function (it) {
      var active = it.id === page ? ' aria-current="page"' : '';
      return '<a href="' + it.href + '"' + active + '>' + (ICONS[it.icon] || ICONS.settings) + ' ' + esc(it.label) + '</a>';
    }).join('');
  }

  /* =====================================================================
     BREADCRUMBS helper
  ===================================================================== */
  function crumbs(items) {
    return '<nav class="crumbs" aria-label="Breadcrumb">' + items.map(function (it, i) {
      var last = i === items.length - 1;
      if (last) return '<span class="current">' + esc(it.label) + '</span>';
      return '<a href="' + it.href + '">' + esc(it.label) + '</a><span class="sep">' + ICONS.chevronRight.replace('width="17"', '') + '</span>';
    }).join('') + '</nav>';
  }
  window.NS.crumbs = crumbs;

  /* =====================================================================
     SKELETON / EMPTY / ERROR renderers
  ===================================================================== */
  function skeletonRows(n, cols) {
    n = n || 5; cols = cols || 4;
    var rows = '';
    for (var i = 0; i < n; i++) {
      var cells = '';
      for (var c = 0; c < cols; c++) { cells += '<td><div class="skeleton sk-line w-' + (c === 0 ? 80 : 60) + '"></div></td>'; }
      rows += '<tr>' + cells + '</tr>';
    }
    return rows;
  }
  window.NS.skeletonRows = skeletonRows;

  function emptyState(title, msg, actionLabel, actionHref) {
    return '<div class="state"><span class="ic">' + ICONS.inboxEmpty + '</span><h3>' + esc(title) + '</h3><p>' + esc(msg) + '</p>' +
      (actionLabel ? '<div class="actions"><a class="btn btn-primary" href="' + (actionHref || '#') + '">' + esc(actionLabel) + '</a></div>' : '') + '</div>';
  }
  window.NS.emptyState = emptyState;

  function errorState(title, msg, retryLabel, onRetry) {
    var id = 'err-' + Date.now();
    setTimeout(function () {
      var b = document.getElementById(id);
      if (b) b.addEventListener('click', onRetry || function () { location.reload(); });
    }, 0);
    return '<div class="state"><span class="ic danger">' + ICONS.alert + '</span><h3>' + esc(title) + '</h3><p>' + esc(msg) + '</p><div class="actions"><button class="btn btn-primary" id="' + id + '">' + esc(retryLabel || 'Try again') + '</button></div></div>';
  }
  window.NS.errorState = errorState;

  /* =====================================================================
     COUNT-UP + generic data-attr wiring
  ===================================================================== */
  function wireCountUp() { document.querySelectorAll('[data-countup]').forEach(animateNumber); }

  /* =====================================================================
     INIT
  ===================================================================== */
  function init() {
    applyTheme(storedTheme());
    injectShell();
    wireThemeToggle();
    wireSidebar();
    wireNotifications();
    wireGlobalActions();
    buildSettingsNav();
    wireTabs();
    wireAccordions();
    wireCountUp();
    renderSparklines();
    window.dispatchEvent(new CustomEvent('ns:ready'));
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  // expose for page scripts
  window.NS = window.NS || {};
  window.NS.modal = openModal;
  window.NS.drawer = openDrawer;
  window.NS.confirm = confirmDialog;
  window.NS.toast = showToast;
  window.NS.applyTheme = applyTheme;
  window.NS.wireTabs = wireTabs;
  window.NS.wireAccordions = wireAccordions;
  window.NS.animateNumber = animateNumber;
})();
