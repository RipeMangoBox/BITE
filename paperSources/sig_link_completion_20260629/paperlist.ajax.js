jQuery(document).ready(function ($) {
  const $table = $('#paperlist');
  if (!$table.length || typeof ajaxmeta === 'undefined') return;

  const $tbody = $table.find('tbody');
  const $tableFrame = $table.closest('.pc-paper-table-figure');
  const INDEX_COLUMNS = 1;
  const FILTER_DELAY = 240;
  const VIRTUAL_TABLE_MIN_ROWS = 1000;
  const VIRTUAL_OVERSCAN_ROWS = 25;
  const VIRTUAL_DEFAULT_ROW_HEIGHT = 38;
  const HIGHLIGHT_ROW_LIMIT = 1000;
  const REVIEW_METRIC_CHANNELS = ['raw', 'std', 'mean', 'min', 'max'];
  const REVIEW_METRIC_START_COLUMN = 4;
  const PAPER_COLUMN_START_COLUMN = 4;
  const COUNTRY_COLOR_MAP = {
    china: '#ff4d4f',
    'united states': '#4d79ff',
    us: '#4d79ff',
    usa: '#4d79ff',
  };
  const HIGHLIGHT_ALPHA = 0.8;

  let batch = 0;
  let nRecords = 0;
  let totalRecords = null;
  let fullTotalRecords = null;
  let isFetchAll = false;
  let isLoading = false;
  let statusColumnIndex = -1;
  let currentSortColumn = null;
  let currentSortAscending = true;
  let filterTimer = null;
  let filterFrame = null;
  let virtualFrame = null;
  let progressFrame = null;
  let progressAnimationStart = 0;
  let progressAnimationFrom = 0;
  let progressAnimationTo = 0;
  let displayedRecordCount = 0;
  let progressRecordHold = null;
  let currentRequest = null;
  let loadGeneration = 0;
  let nextLoadOrder = 1;
  let rowCache = [];
  let filteredEntries = [];
  let fullDatasetLoaded = false;
  let virtualTableActive = false;
  let virtualRowHeight = VIRTUAL_DEFAULT_ROW_HEIGHT;
  let virtualStartIndex = 0;
  let virtualEndIndex = 0;
  let pageIndex = 0;
  let pageSize = 100;
  let renderMode = 'all';
  let columnFilters = [];
  let pendingQueryReplace = false;
  let tableSettingsGui = null;
  let tableSettingsState = null;
  let tableSettingsRenderController = null;
  let tableSettingsRowsController = null;
  let tableSettingsPageController = null;
  const reviewMetricOptions = Array.isArray(ajaxmeta.review_metrics) ? ajaxmeta.review_metrics : [];
  const paperColumnOptions = Array.isArray(ajaxmeta.paper_columns) ? ajaxmeta.paper_columns : [];
  const tableFilterOptions = ajaxmeta.filter_options && typeof ajaxmeta.filter_options === 'object' ? ajaxmeta.filter_options : {};
  let reviewDims = Array.isArray(ajaxmeta.review_dims) ? ajaxmeta.review_dims.slice() : ['rating', 'confidence'];
  let paperDims = Array.isArray(ajaxmeta.paper_dims) ? ajaxmeta.paper_dims.slice() : ['authors', 'affiliations', 'countries'];
  let reviewMetricSearch = normalizeReviewMetricChannel(ajaxmeta.review_metric_search);
  let reviewMetricSearchByDim = {};
  if (ajaxmeta.review_metric_search_map && typeof ajaxmeta.review_metric_search_map === 'object') {
    Object.keys(ajaxmeta.review_metric_search_map).forEach((key) => {
      reviewMetricSearchByDim[key] = normalizeReviewMetricChannel(ajaxmeta.review_metric_search_map[key]);
    });
  }

  ensureTableStyles();
  ensureAuthorPopup();
  syncReviewMetricHeaders();
  syncPaperColumnHeaders();
  updateMultiFilterSummaries();
  findStatusColumnIndex();
  bindControls();
  ensureTableSettingsGui();
  bindHoverHighlighting();
  bindAuthorPopup();
  loadMoreRows();
  window.addEventListener('pc:community-review-saved', function () {
    const reloadAllRecords = hasCompleteLocalDataset();
    resetLoadedRowsForQuery({
      forceServer: true,
      fetchAll: reloadAllRecords,
      holdProgress: reloadAllRecords,
      status: reloadAllRecords ? 'Refreshing full records...' : 'Refreshing...',
    });
  });

  function formatCount(value) {
    const number = Number(value || 0);
    return Number.isFinite(number) ? number.toLocaleString() : '0';
  }

  function cleanText(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function ensureTableStyles() {
    if (document.getElementById('pc-paperlist-ajax-style')) return;
    const css = `
      .pc-paper-table-figure { overflow:auto; }
      #paperlist { border-collapse:separate; border-spacing:0; width:100%; }
      #paperlist .pc-paper-dim-cell { min-width:12ch; max-width:34ch; vertical-align:top; font-size:12px; line-height:1.35; }
      #paperlist .pc-paper-dim-abstract, #paperlist .pc-paper-dim-tldr { min-width:30ch; max-width:54ch; }
      #paperlist .pc-paper-keyword-token { display:inline; border-radius:3px; padding:0 2px; background:rgba(148,163,184,.16); color:#374151; }
      #paperlist .pc-paper-dim-list { max-height:6.5em; overflow:auto; scrollbar-width:thin; }
      #paperlist .pc-paper-links { display:block; margin-top:4px; color:#6b7280; font-size:11px; line-height:1.25; }
      #paperlist .pc-paper-links ul { margin-top:4px; margin-bottom:0; }
      #paperlist .author-link, #paperlist .aff-link, #paperlist .country-link { border-radius:3px; padding:0 2px; transition:background-color .12s ease; }
      #paperlist thead th { position:sticky; top:0; z-index:2; background:#f7f8fb; border-bottom:1px solid #d9dee8; }
      #paperlist .filter-info th { position:relative; top:auto; z-index:3; padding:8px 10px; }
      #paperlist tbody { transition:opacity .12s ease; }
      .pc-paper-table-loading #paperlist tbody, #paperlist.pc-paper-table-loading tbody { opacity:.48; }
      .pc-paper-table-loading #paperlist, #paperlist.pc-paper-table-loading { cursor:progress; }
      #paperlist .pc-virtual-spacer td { height:0; padding:0 !important; border:0 !important; background:transparent !important; line-height:0 !important; font-size:0 !important; }
      #paperlist .pc-row-index { display:inline-flex; flex-direction:column; align-items:center; justify-content:center; gap:0; min-width:4ch; max-width:5.5ch; line-height:1; white-space:nowrap; overflow:hidden; }
      #paperlist .pc-row-base { color:#1f2937; font-size:10px; font-weight:600; line-height:1; white-space:nowrap; }
      #paperlist .pc-row-current { color:#8b96a6; font-size:8px; font-weight:500; line-height:1; white-space:nowrap; }
      #paperlist input { min-height:28px; border:1px solid #c8ced8; border-radius:5px; padding:2px 6px; font-size:12px; }
      #paperlist th.pc-th-sortable { white-space:normal; }
      #paperlist .pc-th-sort { display:inline-flex; align-items:center; justify-content:center; gap:4px; max-width:100%; }
      #paperlist .pc-th-sort-label { min-width:0; }
      #paperlist .sort-btn.pc-sort-btn { display:inline-flex; align-items:center; justify-content:center; flex:0 0 auto; width:18px; height:18px; margin:0; padding:0; border:0; border-radius:50%; background:transparent; color:#8b96a6; box-shadow:none; font:inherit; line-height:1; text-decoration:none; cursor:pointer; opacity:.55; vertical-align:middle; }
      #paperlist th:hover .sort-btn.pc-sort-btn { opacity:.95; }
      #paperlist .sort-btn.pc-sort-btn:hover { color:#374151; background:rgba(15,23,42,.07); }
      #paperlist .sort-btn.pc-sort-btn.pc-sort-active { color:#1f2937; background:#eef2f7; opacity:1; }
      #paperlist .sort-btn.pc-sort-btn:focus-visible { outline:2px solid #6b8afd; outline-offset:2px; }
      #paperlist .pc-sort-icon { display:block; width:12px; height:12px; }
      #paperlist .pc-sort-up, #paperlist .pc-sort-down { fill:currentColor; opacity:.45; }
      #paperlist .pc-sort-btn.pc-sort-asc .pc-sort-up,
      #paperlist .pc-sort-btn.pc-sort-desc .pc-sort-down { opacity:1; }
      #paperlist .pc-sort-btn.pc-sort-asc .pc-sort-down,
      #paperlist .pc-sort-btn.pc-sort-desc .pc-sort-up { opacity:.18; }
      #paperlist .pc-th-stack { display:flex; flex-direction:column; align-items:stretch; justify-content:center; gap:5px; width:100%; max-width:100%; }
      #paperlist .pc-th-stack .pc-th-sort { align-self:center; max-width:100%; }
      #paperlist .pc-th-stack .pc-review-metric-title,
      #paperlist .pc-th-stack .pc-review-metric-search { align-self:center; }
      #paperlist .pc-th-mid-spacer { display:block; flex:0 0 14px; height:14px; min-height:14px; }
      #paperlist .pc-th-search { box-sizing:border-box; width:100%; max-width:100%; min-height:24px; font-size:11px; padding:2px 7px; border-radius:6px; }
      #paperlist .pc-th-search-wide { min-width:24ch; }
      #paperlist .pc-th-search-mid { min-width:12ch; }
      #paperlist .pc-th-search-compact { min-width:9ch; }
      #paperlist .pc-th-multi { position:relative; display:block; width:100%; min-width:12ch; }
      #paperlist .pc-th-multi[data-filter-key="status"] { min-width:9ch; }
      #paperlist .pc-th-multi summary { list-style:none; display:flex; align-items:center; justify-content:center; box-sizing:border-box; width:100%; min-width:0; min-height:24px; padding:2px 22px 2px 8px; border:1px solid #c8ced8; border-radius:6px; background:#fff; color:#374151; cursor:pointer; font-size:11px; font-weight:500; line-height:1.2; white-space:nowrap; position:relative; }
      #paperlist .pc-th-multi summary::-webkit-details-marker { display:none; }
      #paperlist .pc-th-multi summary::after { content:'\\25BE'; position:absolute; right:7px; top:50%; transform:translateY(-50%); color:#8b96a6; font-size:10px; }
      #paperlist .pc-th-multi[open] summary { border-color:#8c96a5; background:#f8fafc; color:#1f2937; }
      #paperlist .pc-th-multi-text { display:block; min-width:0; max-width:100%; overflow:hidden; text-overflow:ellipsis; }
      #paperlist .pc-th-multi-menu { position:absolute; z-index:34; top:calc(100% + 5px); left:0; min-width:max(100%, 190px); max-width:min(360px, 70vw); max-height:260px; overflow:auto; padding:6px; border:1px solid #c8ced8; border-radius:6px; background:#fff; box-shadow:0 10px 24px rgba(15,23,42,.16); text-align:left; }
      #paperlist .pc-th-multi-option { display:flex; align-items:center; gap:6px; margin:0; padding:4px 6px; border-radius:4px; color:#374151; cursor:pointer; font-size:12px; font-weight:400; line-height:1.25; white-space:normal; }
      #paperlist .pc-th-multi-option:hover { background:#edf1f7; }
      #paperlist .pc-th-multi-option input { flex:0 0 auto; min-height:0; margin:0; }
      #paperlist .pc-th-multi-empty { display:block; padding:4px 6px; color:#8b96a6; font-size:12px; white-space:nowrap; }
      #paperlist .pc-session-cell { width:clamp(14ch, 16vw, 28ch); max-width:clamp(14ch, 16vw, 28ch); }
      #paperlist .pc-session-cell small { display:block; max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:11px; line-height:1.2; }
      #paperlist .pc-session-cell a { display:inline; color:inherit; }
      #paperlist .pc-status-cell { width:clamp(9ch, 9vw, 18ch); max-width:clamp(9ch, 9vw, 18ch); }
      #paperlist .pc-status-cell small { display:block; max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:11px; line-height:1.2; }
      #paperlist .pc-review-metric-head { display:inline-flex; flex-direction:column; align-items:center; justify-content:center; gap:1px; min-width:0; }
      #paperlist .pc-review-metric-title { display:inline-flex; align-items:center; justify-content:center; gap:2px; min-width:0; min-height:18px; }
      #paperlist .pc-review-metric-label { display:inline-flex; align-items:center; justify-content:center; gap:4px; min-width:0; }
      #paperlist .pc-review-metric-add,
      #paperlist .pc-review-metric-switch,
      #paperlist .pc-paper-column-add,
      #paperlist .pc-paper-column-switch { position:relative; display:inline-block; }
      #paperlist .pc-review-metric-add summary,
      #paperlist .pc-review-metric-switch summary,
      #paperlist .pc-paper-column-add summary,
      #paperlist .pc-paper-column-switch summary,
      #paperlist .pc-review-metric-remove,
      #paperlist .pc-paper-column-remove { list-style:none; display:inline-flex; align-items:center; justify-content:center; width:17px; height:17px; margin:0; padding:0; border:0; border-radius:50%; background:transparent; color:#8b96a6; box-shadow:none; cursor:pointer; font:inherit; line-height:1; opacity:.72; }
      #paperlist .pc-review-metric-add summary,
      #paperlist .pc-paper-column-add summary { width:auto; min-width:20px; padding:0 6px; border-radius:999px; border:1px solid #c8ced8; background:#fff; color:#4b5563; font-size:11px; font-weight:700; opacity:1; }
      #paperlist .pc-review-metric-add-th,
      #paperlist .pc-review-metric-add-cell,
      #paperlist .pc-paper-column-add-th,
      #paperlist .pc-paper-column-add-cell { width:24px; min-width:24px; max-width:30px; text-align:center; }
      #paperlist .pc-review-metric-add summary::-webkit-details-marker,
      #paperlist .pc-review-metric-switch summary::-webkit-details-marker,
      #paperlist .pc-paper-column-add summary::-webkit-details-marker,
      #paperlist .pc-paper-column-switch summary::-webkit-details-marker { display:none; }
      #paperlist .pc-review-metric-add[open] summary,
      #paperlist .pc-review-metric-switch[open] summary,
      #paperlist .pc-paper-column-add[open] summary,
      #paperlist .pc-paper-column-switch[open] summary,
      #paperlist .pc-review-metric-add summary:hover,
      #paperlist .pc-review-metric-switch summary:hover,
      #paperlist .pc-paper-column-add summary:hover,
      #paperlist .pc-paper-column-switch summary:hover,
      #paperlist .pc-review-metric-remove:hover,
      #paperlist .pc-paper-column-remove:hover { background:#eef2f7; color:#1f2937; opacity:1; }
      #paperlist .pc-review-metric-remove:disabled,
      #paperlist .pc-paper-column-remove:disabled { visibility:hidden; pointer-events:none; }
      #paperlist .pc-review-metric-switch svg,
      #paperlist .pc-paper-column-switch svg { display:block; width:11px; height:11px; fill:currentColor; }
      #paperlist .pc-review-metric-add-menu,
      #paperlist .pc-review-metric-switch-menu { position:absolute; top:calc(100% + 5px); left:50%; transform:translateX(-50%); z-index:32; min-width:170px; max-height:260px; overflow:auto; padding:6px; border:1px solid #c8ced8; border-radius:6px; background:#fff; box-shadow:0 10px 24px rgba(15,23,42,.16); text-align:left; }
      #paperlist .pc-review-metric-switch-menu { left:auto; right:0; transform:none; }
      #paperlist .pc-review-metric-menu-btn { display:block; width:100%; margin:0; padding:4px 7px; border:0; border-radius:4px; background:transparent; color:#374151; cursor:pointer; font-size:12px; line-height:1.3; text-align:left; }
      #paperlist .pc-review-metric-menu-btn:hover { background:#edf1f7; }
      #paperlist .pc-review-metric-menu-btn.is-active { background:#e6edf8; font-weight:700; color:#1f2937; }
      #paperlist .pc-review-metric-menu-empty { display:block; padding:4px 7px; color:#8b96a6; font-size:12px; white-space:nowrap; }
      #paperlist .pc-review-metric-search { display:inline-flex; flex-wrap:nowrap; align-items:center; justify-content:center; gap:0; min-height:14px; margin:0; white-space:nowrap; }
      #paperlist .pc-review-metric-search-label { color:#6b7280; margin-right:2px; }
      #paperlist .pc-review-metric-channel { appearance:none; display:inline-flex; align-items:center; justify-content:center; box-sizing:border-box; width:auto; min-width:0; min-height:0; height:auto; border:0; border-radius:3px; background:transparent; color:#6b7280; box-shadow:none; cursor:pointer; font:inherit; font-size:9px; font-weight:600; line-height:1.2; margin:0; padding:0 2px; text-transform:none; letter-spacing:0; }
      #paperlist .pc-review-metric-channel:hover { background:#edf1f7; color:#374151; }
      #paperlist .pc-review-metric-channel.is-active { background:#dfe8f7; color:#1f2937; box-shadow:inset 0 -2px 0 #6f84b8; }
      #paperlist .pc-review-metric-channel:focus-visible { outline:2px solid #6b8afd; outline-offset:1px; }
      #paperlist .pc-review-metric-search .sort-btn.pc-sort-btn { width:14px; height:14px; margin-left:2px; }
      #paperlist .pc-review-metric-search .pc-sort-icon { width:10px; height:10px; }
      #paperlist .pc-paper-title-cell,
      #paperlist .pc-session-cell,
      #paperlist .pc-status-cell { vertical-align:middle; }
      #paperlist .pc-table-line-stack { display:inline-grid; gap:2px; align-items:center; justify-items:center; white-space:normal; }
      #paperlist .pc-paper-title-cell .pc-table-line-stack { justify-items:start; text-align:left; }
      #paperlist .pc-table-line { display:block; max-width:44ch; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
      #paperlist .pc-review-metric-cell { text-align:center; white-space:normal; }
      #paperlist .pc-review-metric-cell strong { font-size:105%; }
      #paperlist .pc-review-metric-cell small { display:block; color:#5f6876; }
      #paperlist .pc-review-metric-value { max-width:22ch; overflow:hidden; text-overflow:ellipsis; margin:1px auto 0; color:#1f2937; font-weight:600; white-space:pre-line; }
      #paperlist .pc-review-metric-value[hidden] { display:none; }
      .pc-paper-table-toolbar { position:relative; display:flex; flex-wrap:wrap; justify-content:flex-start; align-items:center; gap:8px 14px; width:100%; line-height:1.45; color:inherit; font:inherit; }
      .pc-paper-table-toolbar > * { font:inherit; }
      .pc-paper-table-toolbar small { font-size:12px; line-height:1.3; }
      .pc-paper-table-btn { display:inline-flex; align-items:center; justify-content:center; flex:0 0 auto; min-width:88px; min-height:30px; box-sizing:border-box; border:1px solid #c8ced8; border-radius:5px; background:#fff; color:inherit; cursor:pointer; font-size:12px; line-height:1.2; padding:5px 12px; white-space:nowrap; }
      .pc-paper-table-btn:hover { border-color:#999; }
      .pc-paper-table-btn:disabled { cursor:not-allowed; opacity:.6; }
      .pc-paper-table-nav { min-width:24px; padding-left:6px; padding-right:6px; }
      .pc-paper-table-rows { display:inline-flex; align-items:center; gap:4px; margin:0; }
      .pc-paper-table-rows select { min-height:24px; border:1px solid #c8ced8; border-radius:5px; background:#fff; color:inherit; font-size:12px; padding:1px 5px; }
      .pc-paper-table-load { display:inline-flex; align-items:center; gap:8px; flex:1 1 520px; min-width:min(360px, 100%); min-height:30px; box-sizing:border-box; padding:0 4px; }
      .pc-paper-table-progress-label { white-space:nowrap; font-size:12px; font-weight:600; line-height:1.3; color:#4b5563; }
      .pc-paper-table-count { white-space:nowrap; }
      .pc-paper-table-gear { gap:6px; min-width:98px; height:30px; padding:5px 12px; border-radius:5px; color:#4b5563; }
      .pc-paper-table-gear:hover,
      .pc-paper-table-gear.is-open { border-color:#8c96a5; background:#f8fafc; color:#1f2937; }
      .pc-paper-table-gear-icon { display:block; transform-origin:50% 50%; transition:transform 600ms ease; }
      .pc-paper-table-gear-label { font-size:12px; line-height:1; }
      .pc-paper-table-gear:hover .pc-paper-table-gear-icon,
      .pc-paper-table-gear:focus-visible .pc-paper-table-gear-icon,
      .pc-paper-table-gear.is-open .pc-paper-table-gear-icon { transform:rotate(120deg); }
      .pc-paper-table-help-wrap { position:relative; display:inline-flex; align-items:center; }
      .pc-paper-table-help-toggle { gap:6px; min-width:78px; }
      .pc-paper-table-help-toggle:hover,
      .pc-paper-table-help-toggle.is-open { border-color:#8c96a5; background:#f8fafc; color:#1f2937; }
      .pc-paper-table-help-toggle input { min-height:0 !important; margin:0; }
      .pc-paper-table-help-panel { position:absolute; top:calc(100% + 8px); right:0; z-index:35; width:min(520px, calc(100vw - 48px)); max-height:min(420px, 70vh); overflow:auto; padding:10px 12px; border:1px solid #c8ced8; border-radius:8px; background:#fff; box-shadow:0 12px 28px rgba(15,23,42,.16); color:#374151; font-size:12px; line-height:1.45; text-align:left; }
      .pc-paper-table-help-panel[hidden] { display:none; }
      .pc-paper-table-help-panel b { color:#1f2937; }
      .pc-paper-table-help-panel code { font-size:11px; }
      .pc-paper-table-settings { position:absolute; top:calc(100% + 8px); right:10px; z-index:35; display:grid; grid-template-columns:1fr; gap:8px; min-width:220px; max-width:min(300px, calc(100vw - 48px)); padding:10px; border:1px solid #c8ced8; border-radius:8px; background:#fff; box-shadow:0 12px 28px rgba(15,23,42,.16); text-align:left; }
      .pc-paper-table-settings::before { content:''; position:absolute; top:-6px; right:14px; width:10px; height:10px; border-left:1px solid #c8ced8; border-top:1px solid #c8ced8; background:#fff; transform:rotate(45deg); }
      .pc-paper-table-settings[hidden] { display:none; }
      .pc-paper-table-settings label { display:flex; align-items:center; gap:6px; margin:0; color:#374151; font-size:12px; line-height:1.25; white-space:nowrap; }
      .pc-paper-table-settings input { min-height:0; margin:0; }
      .pc-paper-table-settings .pc-paper-table-rows { justify-content:space-between; gap:10px; }
      .pc-paper-table-page-controls { display:flex; align-items:center; justify-content:space-between; gap:8px; padding-top:6px; border-top:1px solid #edf1f7; }
      .pc-paper-table-page-controls #pc_page_state { color:#6b7280; font-size:12px; white-space:nowrap; }
      .pc-paper-table-gui { position:absolute !important; top:calc(100% + 8px) !important; right:10px !important; left:auto !important; z-index:36 !important; width:260px !important; max-width:calc(100vw - 48px); --font-size:11px; --input-font-size:11px; --widget-height:20px; --padding:4px; --spacing:4px; --background-color:rgba(26,26,26,.72); --widget-color:rgba(66,66,66,.82); --title-background-color:rgba(17,17,17,.72); --text-color:#eee; --number-color:#a8d8ff; --string-color:#9bdca8; font-size:11px !important; }
      .pc-paper-table-gui .title { padding-right:28px; font-size:11px !important; line-height:20px !important; }
      #paperlist .pc-paper-table-gui input,
      #paperlist .pc-paper-table-gui select { min-height:0 !important; height:20px !important; font-size:11px !important; line-height:18px !important; padding-top:0 !important; padding-bottom:0 !important; border-radius:2px !important; }
      .pc-paper-table-gui .pc-table-gui-close { position:absolute; top:2px; right:4px; width:20px; height:20px; padding:0; border:0; background:transparent; color:#ccc; cursor:pointer; font:600 18px/1 sans-serif; z-index:10; }
      .pc-paper-table-gui .pc-table-gui-close:hover { color:#fff; }
      .pc-paper-table-gui .pc-table-gui-readonly input { pointer-events:none; opacity:.82; }
      .pc-paper-table-gui .pc-table-gui-readonly .name { color:#cfd6df; }
      .pc-paper-table-gui .pc-table-gui-source { display:block; padding:6px 8px 7px; border-top:1px solid rgba(255,255,255,.12); color:#cfd6df; font-size:11px; line-height:1.3; }
      .pc-paper-table-gui .pc-table-gui-source a { color:#a8d8ff; text-decoration:none; }
      .pc-paper-table-gui .pc-table-gui-source a:hover { text-decoration:underline; }
      .pc-paper-table-page-controls { display:inline-flex; align-items:center; gap:6px; white-space:nowrap; }
      .pc-paper-table-status { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
      .pc-paper-table-source { display:block; padding-top:6px; border-top:1px solid #edf1f7; color:#6b7280; font-size:12px; line-height:1.3; white-space:normal; }
      .pc-paper-table-source a { text-decoration:none; }
      .pc-paper-table-source a:hover { text-decoration:underline; }
      @keyframes pc-progress-reload-sweep { from { transform:translateX(-100%); } to { transform:translateX(260%); } }
      .pc-paper-table-progress { --pc-reload-progress:0%; flex:1 1 180px; min-width:120px; height:5px; overflow:hidden; border-radius:999px; background:#eceff3; }
      .pc-paper-table-progress span { position:relative; display:block; width:0%; height:100%; overflow:hidden; background:#9aa4b2; will-change:width; }
      .pc-paper-table-progress.pc-progress-reloading span::after { content:''; position:absolute; left:0; top:0; bottom:0; width:var(--pc-reload-progress); background:#38bdf8; transition:width .24s ease; }
      .pc-paper-table-progress.pc-progress-reloading span::before { content:''; position:absolute; top:0; bottom:0; left:0; z-index:1; width:34%; background:linear-gradient(90deg, transparent, rgba(255,255,255,.55), transparent); animation:pc-progress-reload-sweep 1.05s linear infinite; }
      #paperlist mark.pc-search-hit { background:#fff1a8; color:inherit; border-radius:2px; padding:0 .08em; box-decoration-break:clone; -webkit-box-decoration-break:clone; }
      #author-popup { position:absolute; display:none; max-width:min(360px, calc(100vw - 28px)); padding:10px 14px; background:#fff; border:1px solid #b9c2d0; border-radius:7px; font-size:13px; z-index:10000; box-shadow:0 10px 24px rgba(15,23,42,.16); line-height:1.55; }
      #author-popup a { color:#0645ad; text-decoration:none; display:block; margin-top:4px; }
      #author-popup a:hover { text-decoration:underline; }
    `;
    document.head.appendChild(Object.assign(document.createElement('style'), {
      id: 'pc-paperlist-ajax-style',
      textContent: css,
    }));
  }

  function ensureAuthorPopup() {
    if ($('#author-popup').length) return;
    $('body').append('<div id="author-popup" aria-live="polite"></div>');
  }

  function parsePayload(data) {
    if (data === '0' || data === 0 || data == null) {
      return { html: '', count: 0, total: totalRecords, has_more: false };
    }
    if (typeof data === 'object') {
      const html = data.html || '';
      return {
        html,
        count: Number.isFinite(Number(data.count)) ? Number(data.count) : countRowsInHtml(html),
        total: Number.isFinite(Number(data.total)) ? Number(data.total) : totalRecords,
        has_more: typeof data.has_more === 'boolean' ? data.has_more : html.length > 0,
      };
    }
    const html = String(data || '');
    return {
      html,
      count: countRowsInHtml(html),
      total: totalRecords,
      has_more: html.length > 0,
    };
  }

  function countRowsInHtml(html) {
    return (String(html || '').match(/<tr(?:\s|>)/gi) || []).length;
  }

  function hasActiveColumnFilters() {
    return columnFilters.length > 0;
  }

  function loadMoreRows() {
    if (isLoading) return;
    isLoading = true;
    setTableLoading($tbody.children().length > 0);
    updateLoadStatus('Loading...');

    const generation = loadGeneration;
    const requestData = {
      action: 'load_paperlist',
      batch,
      conf: ajaxmeta.conf,
      year: ajaxmeta.year,
      mode: ajaxmeta.mode,
      track: ajaxmeta.track,
      surface: ajaxmeta.surface || 'papers',
      filters: JSON.stringify(columnFilters),
    };
    if (ajaxmeta.mode === 'rating') {
      requestData.review_dims = JSON.stringify(reviewDims);
      requestData.review_metric_search = reviewMetricSearch;
      requestData.review_metric_search_map = JSON.stringify(reviewMetricSearchMapForRequest());
    } else if (ajaxmeta.mode === 'detail') {
      requestData.paper_dims = JSON.stringify(paperDims);
    }

    currentRequest = $.ajax({
      url: ajaxmeta.ajax_url,
      type: 'GET',
      data: requestData,
      success(data) {
        if (generation !== loadGeneration) return;
        const payload = parsePayload(data);
        if (payload.total !== null && payload.total !== undefined) {
          const payloadTotal = Number(payload.total);
          totalRecords = payloadTotal;
          if (!hasActiveColumnFilters() && Number.isFinite(payloadTotal)) {
            fullTotalRecords = payloadTotal;
          }
        }

        replacePendingRowsIfNeeded();

        if (!payload.html) {
          finishLoading(payload.has_more);
          applyFiltersNow();
          return;
        }

        const $rows = appendRows(payload.html);
        batch += 1;
        nRecords += $rows.length;

        applyActiveDisplayModes($rows);
        applyReviewMetricSearchChannel($rows);
        cacheRows($rows);
        const hasMore = payload.has_more !== false && (totalRecords === null || nRecords < totalRecords);

        if (!(isFetchAll && hasMore)) {
          applyActiveOrder();
        }
        updateRecordStats();

        if (isFetchAll && hasMore) {
          isLoading = false;
          window.setTimeout(loadMoreRows, 0);
          return;
        }

        applyFiltersNow();
        finishLoading(hasMore);
      },
      error(xhr, status, error) {
        if (status === 'abort') return;
        isLoading = false;
        progressRecordHold = null;
        if (pendingQueryReplace) {
          pendingQueryReplace = false;
          nRecords = rowCache.length;
          totalRecords = null;
          updateRecordStats();
        }
        setTableLoading(false);
        updateLoadStatus('Load failed. Try again.');
        $('#btn_fetchall').prop('disabled', false).text('Fetch all');
        console.error('Paper list AJAX error:', status, error, xhr && xhr.responseText);
      },
      complete() {
        if (generation === loadGeneration) {
          currentRequest = null;
        }
      },
    });
  }

  function appendRows(html) {
    const $holder = $('<tbody></tbody>').html(html);
    return $holder.children('tr');
  }

  function finishLoading(hasMore) {
    const done = !hasMore || (totalRecords !== null && nRecords >= totalRecords);
    isLoading = false;
    if (done) progressRecordHold = null;
    updateRecordStats();
    if (done) {
      if (!hasActiveColumnFilters()) fullDatasetLoaded = true;
      const filteredQuery = hasActiveColumnFilters() && !hasCompleteLocalDataset();
      $('#btn_fetchall').prop('disabled', true).text(filteredQuery ? 'All matches loaded' : 'All loaded');
      updateLoadStatus(filteredQuery ? 'All matching rows are loaded.' : 'All available rows are loaded.');
    } else if (isFetchAll) {
      $('#btn_fetchall').prop('disabled', false).text('Fetch all');
      updateLoadStatus('Paused before the next batch.');
    } else {
      $('#btn_fetchall').prop('disabled', false).text('Fetch all');
      updateLoadStatus('Loaded first batch. Fetch all to search the full dataset.');
    }
  }

  function currentProgressValue() {
    const raw = $('#pc_load_progress').css('width');
    const bar = $('#pc_load_progress').parent()[0];
    const px = parseFloat(raw);
    const total = bar ? bar.getBoundingClientRect().width : 0;
    if (!Number.isFinite(px) || !total) return progressAnimationTo || 0;
    return Math.max(0, Math.min(100, (px / total) * 100));
  }

  function setProgressDisplay(percent, recordCount, options) {
    const opts = options || {};
    const target = Math.max(0, Math.min(100, Number(percent) || 0));
    const targetCount = Math.max(0, Number(recordCount) || 0);
    if (progressFrame) {
      window.cancelAnimationFrame(progressFrame);
      progressFrame = null;
    }
    if (opts.instant) {
      progressAnimationTo = target;
      displayedRecordCount = targetCount;
      $('#pc_load_progress').css('width', `${target}%`);
      $('#n_records').text(formatCount(targetCount));
      return;
    }

    progressAnimationFrom = currentProgressValue();
    progressAnimationTo = target;
    const countFrom = displayedRecordCount;
    const countTo = targetCount;
    progressAnimationStart = window.performance && window.performance.now ? window.performance.now() : Date.now();
    const percentDelta = Math.abs(progressAnimationTo - progressAnimationFrom);
    const countDelta = Math.abs(countTo - countFrom);
    const duration = Math.max(420, Math.min(1400, Math.max(percentDelta * 38, countDelta * 2.5)));

    const step = function (now) {
      const elapsed = now - progressAnimationStart;
      const t = Math.max(0, Math.min(1, elapsed / duration));
      const eased = 1 - Math.pow(1 - t, 3);
      const value = progressAnimationFrom + ((progressAnimationTo - progressAnimationFrom) * eased);
      const count = Math.round(countFrom + ((countTo - countFrom) * eased));
      $('#pc_load_progress').css('width', `${value}%`);
      $('#n_records').text(formatCount(count));
      if (t < 1) {
        progressFrame = window.requestAnimationFrame(step);
      } else {
        displayedRecordCount = countTo;
        $('#n_records').text(formatCount(countTo));
        progressFrame = null;
      }
    };
    progressFrame = window.requestAnimationFrame(step);
  }

  function updateProgressReloadState(denominator) {
    const $bar = $('#pc_load_progress').parent();
    const active = progressRecordHold !== null;
    if (!active) {
      $bar.removeClass('pc-progress-reloading').css('--pc-reload-progress', '0%');
      return;
    }
    const denom = Number(denominator) || Number(totalRecords) || Number(fullTotalRecords) || 0;
    const pct = denom > 0 ? Math.max(0, Math.min(100, (nRecords / denom) * 100)) : 0;
    $bar.addClass('pc-progress-reloading').css('--pc-reload-progress', `${pct}%`);
  }

  function updateRecordStats() {
    const denominator = fullTotalRecords !== null && Number.isFinite(fullTotalRecords)
      ? fullTotalRecords
      : totalRecords;
    const displayedCount = currentProgressRecordCount();
    updateProgressReloadState(denominator);
    if (denominator !== null && Number.isFinite(denominator)) {
      $('#pc_total_records').text(` / ${formatCount(denominator)}`);
      const pct = denominator > 0 ? Math.min(100, (displayedCount / denominator) * 100) : 0;
      setProgressDisplay(pct, displayedCount);
      $('#pc_load_percent').text(` (${Math.round(pct)}%)`);
    } else {
      $('#pc_total_records').text(' / ...');
      setProgressDisplay(0, displayedCount, { instant: true });
      $('#pc_load_percent').text('');
    }
    const fullLoaded = fullTotalRecords !== null && nRecords >= fullTotalRecords && !hasActiveColumnFilters();
    if (fullLoaded) {
      $('#pc_load_status').text('All available rows are loaded.');
    }
  }

  function currentProgressRecordCount() {
    if (progressRecordHold !== null && isLoading) {
      return progressRecordHold;
    }
    if (hasCompleteLocalDataset() && hasActiveColumnFilters()) {
      return filteredEntries.length;
    }
    return nRecords;
  }

  function updateLoadStatus(text) {
    $('#pc_load_status').text(text);
  }

  function hasAllRecordsLoaded() {
    if (totalRecords === null) return fullDatasetLoaded && !isLoading;
    return Number.isFinite(Number(totalRecords)) && rowCache.length >= Number(totalRecords);
  }

  function hasCompleteLocalDataset() {
    return fullDatasetLoaded && hasAllRecordsLoaded();
  }

  function setTableLoading(isBusy) {
    $table.toggleClass('pc-paper-table-loading', isBusy).attr('aria-busy', isBusy ? 'true' : 'false');
    $tableFrame.toggleClass('pc-paper-table-loading', isBusy);
  }

  function replacePendingRowsIfNeeded() {
    if (!pendingQueryReplace) return;
    disableVirtualTable();
    rowCache = [];
    filteredEntries = [];
    nextLoadOrder = 1;
    // Keep the old rendered rows in place while search fetch-all streams batches,
    // so page height does not collapse and trigger global nav show/hide flicker.
    if (!isFetchAll) {
      clearRenderedRows();
    }
    pendingQueryReplace = false;
  }

  function escapeHtml(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function isReviewMetricTable() {
    return ajaxmeta.mode === 'rating' && reviewMetricOptions.length > 0;
  }

  function isPaperColumnTable() {
    return ajaxmeta.mode === 'detail' && paperColumnOptions.length > 0;
  }

  function reviewMetricLabel(key) {
    const match = reviewMetricOptions.find((metric) => metric && metric.key === key);
    return match ? match.label : cleanText(key).replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function paperColumnLabel(key) {
    const match = paperColumnOptions.find((column) => column && column.key === key);
    return match ? match.label : cleanText(key).replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }

  function normalizeReviewMetricChannel(value) {
    return REVIEW_METRIC_CHANNELS.includes(value) ? value : 'raw';
  }

  function syncReviewMetricChannelState() {
    const selected = new Set(reviewDims);
    reviewDims.forEach((key) => {
      reviewMetricSearchByDim[key] = normalizeReviewMetricChannel(reviewMetricSearchByDim[key] || reviewMetricSearch);
    });
    Object.keys(reviewMetricSearchByDim).forEach((key) => {
      if (!selected.has(key)) delete reviewMetricSearchByDim[key];
    });
  }

  function reviewMetricChannelFor(key) {
    if (!key) return normalizeReviewMetricChannel(reviewMetricSearch);
    reviewMetricSearchByDim[key] = normalizeReviewMetricChannel(reviewMetricSearchByDim[key] || reviewMetricSearch);
    return reviewMetricSearchByDim[key];
  }

  function reviewMetricSearchMapForRequest() {
    syncReviewMetricChannelState();
    const map = {};
    reviewDims.forEach((key) => {
      map[key] = reviewMetricChannelFor(key);
    });
    return map;
  }

  function reviewMetricSearchLabel(key) {
    const labels = { raw: 'Raw', std: 'Std', mean: 'Mean', min: 'Min', max: 'Max' };
    return labels[reviewMetricChannelFor(key)] || 'Raw';
  }

  function buildSortButtonHtml(colIndex, label) {
    const safeLabel = escapeHtml(label);
    return `<button type="button" class="sort-btn pc-sort-btn" data-col="${colIndex}" data-sort-name="${safeLabel}" aria-label="Sort ${safeLabel}" title="Sort ${safeLabel}"><svg class="pc-sort-icon" width="12" height="12" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path class="pc-sort-up" d="M6 2 2.8 5.2h6.4L6 2z"></path><path class="pc-sort-down" d="M6 10 2.8 6.8h6.4L6 10z"></path></svg></button>`;
  }

  function buildSortHeaderHtml(labelHtml, colIndex, labelText, extraClass) {
    return `<th class="pc-th-sortable${extraClass ? ` ${extraClass}` : ''}" aria-sort="none"><span class="pc-th-sort"><span class="pc-th-sort-label">${labelHtml}</span>${buildSortButtonHtml(colIndex, labelText)}</span></th>`;
  }

  function buildHeaderSearchHtml(colIndex, placeholder, extraClass) {
    return `<input type="search" class="pc-th-search${extraClass ? ` ${extraClass}` : ''}" data-col="${colIndex}" placeholder="${escapeHtml(placeholder)}">`;
  }

  function buildSearchSortHeaderHtml(labelHtml, colIndex, labelText, placeholder, inputClass, extraClass) {
    return `<th class="pc-th-sortable${extraClass ? ` ${extraClass}` : ''}" aria-sort="none"><span class="pc-th-stack"><span class="pc-th-sort"><span class="pc-th-sort-label">${labelHtml}</span>${buildSortButtonHtml(colIndex, labelText)}</span><span class="pc-th-mid-spacer" aria-hidden="true"></span>${buildHeaderSearchHtml(colIndex, placeholder, inputClass)}</span></th>`;
  }

  function tableFilterOptionList(optionKey) {
    const rawOptions = Array.isArray(tableFilterOptions[optionKey]) ? tableFilterOptions[optionKey] : [];
    return rawOptions.map((option) => {
      if (option && typeof option === 'object') {
        return {
          value: cleanText(option.value || option.label),
          label: cleanText(option.label || option.value),
        };
      }
      const value = cleanText(option);
      return { value, label: value };
    }).filter((option) => option.value);
  }

  function buildHeaderMultiFilterHtml(colIndex, optionKey, labelText) {
    const options = tableFilterOptionList(optionKey);
    const choices = options.length
      ? options.map((option) => `<label class="pc-th-multi-option"><input type="checkbox" class="pc-th-filter-choice" data-col="${colIndex}" value="${escapeHtml(option.value)}"><span>${escapeHtml(option.label)}</span></label>`).join('')
      : '<span class="pc-th-multi-empty">No options</span>';
    return `<details class="pc-th-multi" data-col="${colIndex}" data-filter-key="${escapeHtml(optionKey)}"><summary title="Filter ${escapeHtml(labelText)}" aria-label="Filter ${escapeHtml(labelText)}"><span class="pc-th-multi-text">All</span></summary><div class="pc-th-multi-menu">${choices}</div></details>`;
  }

  function buildMultiFilterSortHeaderHtml(labelHtml, colIndex, labelText, optionKey, extraClass) {
    return `<th class="pc-th-sortable${extraClass ? ` ${extraClass}` : ''}" aria-sort="none"><span class="pc-th-stack"><span class="pc-th-sort"><span class="pc-th-sort-label">${labelHtml}</span>${buildSortButtonHtml(colIndex, labelText)}</span><span class="pc-th-mid-spacer" aria-hidden="true"></span>${buildHeaderMultiFilterHtml(colIndex, optionKey, labelText)}</span></th>`;
  }

  function updateMultiFilterSummaries(scope) {
    const $scope = scope ? $(scope) : $table;
    const $filters = $scope.is && $scope.is('.pc-th-multi') ? $scope : $scope.find('.pc-th-multi');
    $filters.each(function () {
      const $filter = $(this);
      const $checked = $filter.find('.pc-th-filter-choice:checked');
      const compactSelectionText = String($filter.data('filterKey') || '') === 'session';
      let text = 'All';
      if (compactSelectionText && $checked.length > 0) {
        text = `${$checked.length} selected`;
      } else if ($checked.length === 1) {
        text = cleanText($checked.first().closest('label').text()) || '1 selected';
      } else if ($checked.length > 1) {
        text = `${$checked.length} selected`;
      }
      $filter.find('.pc-th-multi-text').text(text);
      $filter.find('summary').attr('title', text === 'All' ? 'All' : text);
    });
  }

  function metricOptionsHtml(currentKey, options) {
    if (!options.length) return '<span class="pc-review-metric-menu-empty">No more metrics</span>';
    return options.map((metric) => {
      const key = metric.key;
      const active = key === currentKey;
      return `<button type="button" class="pc-review-metric-menu-btn${active ? ' is-active' : ''}" data-metric-key="${escapeHtml(key)}">${escapeHtml(metric.label)}</button>`;
    }).join('');
  }

  function buildReviewMetricAddHtml() {
    const remaining = reviewMetricOptions.filter((metric) => !reviewDims.includes(metric.key));
    return `<details class="pc-review-metric-add"><summary title="Add review metric" aria-label="Add review metric">+</summary><div class="pc-review-metric-add-menu">${metricOptionsHtml('', remaining)}</div></details>`;
  }

  function buildReviewMetricSwitchHtml(key, index, labelText) {
    return `<details class="pc-review-metric-switch" data-metric-index="${index}"><summary title="Switch ${escapeHtml(labelText)} metric" aria-label="Switch ${escapeHtml(labelText)} metric"><svg width="11" height="11" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M3 4h6L6 8 3 4z"></path></svg></summary><div class="pc-review-metric-switch-menu">${metricOptionsHtml(key, reviewMetricOptions)}</div></details>`;
  }

  function buildReviewMetricRemoveHtml(key, labelText) {
    const disabled = reviewDims.length <= 1 ? ' disabled' : '';
    return `<button type="button" class="pc-review-metric-remove" data-metric-dim="${escapeHtml(key)}" title="Remove ${escapeHtml(labelText)} metric" aria-label="Remove ${escapeHtml(labelText)} metric"${disabled}>×</button>`;
  }

  function buildReviewMetricSearchHtml(key, labelText, colIndex) {
    const current = reviewMetricChannelFor(key);
    const channels = [
      ['raw', 'Raw'],
      ['std', 'Std'],
      ['mean', 'Mean'],
      ['min', 'Min'],
      ['max', 'Max'],
    ].map(([value, label]) => {
      const active = current === value;
      return `<button type="button" class="pc-review-metric-channel${active ? ' is-active' : ''}" data-metric-dim="${escapeHtml(key)}" data-channel="${value}" aria-pressed="${active ? 'true' : 'false'}">${label}</button>`;
    }).join('');
    return `<span class="pc-review-metric-search" role="group" aria-label="${escapeHtml(labelText)} search and sort channel">${channels}${buildSortButtonHtml(colIndex, labelText)}</span>`;
  }

  function syncReviewMetricHeaders() {
    if (!isReviewMetricTable()) return;
    const allowed = new Set(reviewMetricOptions.map((metric) => metric.key));
    reviewDims = reviewDims.filter((key) => allowed.has(key));
    if (!reviewDims.length) {
      reviewDims = reviewMetricOptions
        .filter((metric) => metric.key === 'rating' || metric.key === 'confidence')
        .map((metric) => metric.key);
    }
    if (!reviewDims.length && reviewMetricOptions[0]) reviewDims = [reviewMetricOptions[0].key];
    syncReviewMetricChannelState();

    const $header = $table.find('thead tr.pc-review-header-row');
    const $thead = $table.find('thead');
    $table.find('thead tr.pc-review-metric-control-row').remove();
    $table.find('thead tr.filter-row').remove();
    if (!$header.length) return;
    const filterValues = {};
    const multiValues = {};
    $thead.find('input.pc-th-search').each(function () {
      const colIndex = parseInt($(this).data('col'), 10);
      if (!Number.isNaN(colIndex)) filterValues[colIndex] = $(this).val();
    });
    $thead.find('.pc-th-filter-choice:checked').each(function () {
      const colIndex = parseInt($(this).data('col'), 10);
      if (Number.isNaN(colIndex)) return;
      if (!multiValues[colIndex]) multiValues[colIndex] = [];
      multiValues[colIndex].push($(this).val());
    });

    const headerParts = [
      '<th></th>',
      buildSearchSortHeaderHtml('Title', 1, 'Title', 'Search title', 'pc-th-search-wide'),
      buildMultiFilterSortHeaderHtml('Session/Area', 2, 'Session/Area', 'session'),
      buildMultiFilterSortHeaderHtml('Status', REVIEW_METRIC_START_COLUMN - 1, 'Status', 'status'),
    ];

    reviewDims.forEach((key, index) => {
      const colIndex = REVIEW_METRIC_START_COLUMN + index;
      const label = reviewMetricLabel(key);
      const labelHtml = `<span class="pc-th-stack"><span class="pc-review-metric-title">${buildReviewMetricRemoveHtml(key, label)}<span class="pc-review-metric-label">${escapeHtml(label)}</span>${buildReviewMetricSwitchHtml(key, index, label)}</span>${buildReviewMetricSearchHtml(key, label, colIndex)}${buildHeaderSearchHtml(colIndex, `Search ${reviewMetricSearchLabel(key).toLowerCase()}`, 'pc-th-search-compact')}</span>`;
      headerParts.push(`<th class="pc-th-sortable pc-review-metric-th" aria-sort="none">${labelHtml}</th>`);
    });

    headerParts.push(`<th class="pc-review-metric-add-th">${buildReviewMetricAddHtml()}</th>`);

    $header.html(headerParts.join(''));
    Object.keys(filterValues).forEach((colIndex) => {
      $thead.find(`input.pc-th-search[data-col="${colIndex}"]`).val(filterValues[colIndex]);
    });
    Object.keys(multiValues).forEach((colIndex) => {
      const selected = multiValues[colIndex];
      $thead.find(`.pc-th-filter-choice[data-col="${colIndex}"]`).each(function () {
        $(this).prop('checked', selected.includes($(this).val()));
      });
    });
    updateMultiFilterSummaries($thead);
    $table.find('.pc-paper-table-toolbar-cell').attr('colspan', 5 + reviewDims.length);
    findStatusColumnIndex();
    syncSortButtons();
  }

  function paperColumnOptionsHtml(currentKey, selectedKeys) {
    const selected = new Set(selectedKeys || []);
    const options = paperColumnOptions.filter((column) => currentKey || !selected.has(column.key));
    if (!options.length) return '<span class="pc-review-metric-menu-empty">No more columns</span>';
    return options.map((column) => {
      const active = column.key === currentKey;
      return `<button type="button" class="pc-review-metric-menu-btn pc-paper-column-menu-btn${active ? ' is-active' : ''}" data-paper-column-key="${escapeHtml(column.key)}">${escapeHtml(column.label)}</button>`;
    }).join('');
  }

  function buildPaperColumnAddHtml() {
    return `<details class="pc-paper-column-add"><summary title="Add paper column" aria-label="Add paper column">+</summary><div class="pc-review-metric-add-menu pc-paper-column-add-menu">${paperColumnOptionsHtml('', paperDims)}</div></details>`;
  }

  function buildPaperColumnSwitchHtml(key, index, labelText) {
    return `<details class="pc-paper-column-switch" data-paper-column-index="${index}"><summary title="Switch ${escapeHtml(labelText)} column" aria-label="Switch ${escapeHtml(labelText)} column"><svg width="11" height="11" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M3 4h6L6 8 3 4z"></path></svg></summary><div class="pc-review-metric-switch-menu pc-paper-column-switch-menu">${paperColumnOptionsHtml(key, paperDims)}</div></details>`;
  }

  function buildPaperColumnRemoveHtml(key, labelText) {
    const disabled = paperDims.length <= 1 ? ' disabled' : '';
    return `<button type="button" class="pc-paper-column-remove" data-paper-column-key="${escapeHtml(key)}" title="Remove ${escapeHtml(labelText)} column" aria-label="Remove ${escapeHtml(labelText)} column"${disabled}>×</button>`;
  }

  function syncPaperColumnHeaders() {
    if (!isPaperColumnTable()) return;
    const allowed = new Set(paperColumnOptions.map((column) => column.key));
    paperDims = paperDims.filter((key) => allowed.has(key));
    if (!paperDims.length) {
      paperDims = paperColumnOptions
        .filter((column) => column.key === 'authors' || column.key === 'affiliations' || column.key === 'countries')
        .map((column) => column.key);
    }
    if (!paperDims.length && paperColumnOptions[0]) paperDims = [paperColumnOptions[0].key];

    const $header = $table.find('thead tr.pc-paper-detail-header-row');
    const $thead = $table.find('thead');
    if (!$header.length) return;
    const filterValues = {};
    const multiValues = {};
    $thead.find('input.pc-th-search').each(function () {
      const colIndex = parseInt($(this).data('col'), 10);
      if (!Number.isNaN(colIndex)) filterValues[colIndex] = $(this).val();
    });
    $thead.find('.pc-th-filter-choice:checked').each(function () {
      const colIndex = parseInt($(this).data('col'), 10);
      if (Number.isNaN(colIndex)) return;
      if (!multiValues[colIndex]) multiValues[colIndex] = [];
      multiValues[colIndex].push($(this).val());
    });

    const headerParts = [
      '<th></th>',
      buildSearchSortHeaderHtml('Title', 1, 'Title', 'Search title', 'pc-th-search-wide'),
      buildMultiFilterSortHeaderHtml('Session/Area', 2, 'Session/Area', 'session'),
      buildMultiFilterSortHeaderHtml('Status', PAPER_COLUMN_START_COLUMN - 1, 'Status', 'status'),
    ];

    paperDims.forEach((key, index) => {
      const colIndex = PAPER_COLUMN_START_COLUMN + index;
      const label = paperColumnLabel(key);
      const labelHtml = `<span class="pc-th-stack"><span class="pc-review-metric-title pc-paper-column-title">${buildPaperColumnRemoveHtml(key, label)}<span class="pc-review-metric-label pc-paper-column-label">${escapeHtml(label)}</span>${buildPaperColumnSwitchHtml(key, index, label)}</span><span class="pc-review-metric-search">${buildSortButtonHtml(colIndex, label)}</span>${buildHeaderSearchHtml(colIndex, `Search ${label.toLowerCase()}`, 'pc-th-search-mid')}</span>`;
      headerParts.push(`<th class="pc-th-sortable pc-paper-column-th" aria-sort="none">${labelHtml}</th>`);
    });

    headerParts.push(`<th class="pc-review-metric-add-th pc-paper-column-add-th">${buildPaperColumnAddHtml()}</th>`);

    $header.html(headerParts.join(''));
    Object.keys(filterValues).forEach((colIndex) => {
      $thead.find(`input.pc-th-search[data-col="${colIndex}"]`).val(filterValues[colIndex]);
    });
    Object.keys(multiValues).forEach((colIndex) => {
      const selected = multiValues[colIndex];
      $thead.find(`.pc-th-filter-choice[data-col="${colIndex}"]`).each(function () {
        $(this).prop('checked', selected.includes($(this).val()));
      });
    });
    updateMultiFilterSummaries($thead);
    $table.find('.pc-paper-table-toolbar-cell').attr('colspan', 5 + paperDims.length);
    findStatusColumnIndex();
    syncSortButtons();
  }

  function findStatusColumnIndex() {
    statusColumnIndex = -1;
    const headerRows = $table.find('thead tr').not('.filter-info');
    headerRows.last().children('th').each(function (index) {
      const label = cleanText($(this).clone().find('.sort-btn').remove().end().text()).toLowerCase();
      if (label === 'status') {
        statusColumnIndex = index;
        return false;
      }
      return true;
    });
  }

  function cacheRows($rows) {
    if (statusColumnIndex === -1) findStatusColumnIndex();
    $rows.each(function () {
      const entry = buildRowEntry(this);
      rowCache.push(entry);
    });
  }

  function buildRowEntry(row) {
    if (!row.dataset.pcLoadOrder) {
      row.dataset.pcLoadOrder = String(nextLoadOrder);
      nextLoadOrder += 1;
    }
    const cells = Array.from(row.cells).map((cell) => {
      const text = cleanText(cell.dataset.search || cell.textContent).toLowerCase();
      cell.dataset.val = cleanText(cell.textContent);
      return text;
    });
    const status = statusColumnIndex >= 0 ? (cells[statusColumnIndex] || '') : '';
    const searchText = cells.slice(INDEX_COLUMNS).join(' ');
    const loadOrder = parseInt(row.dataset.pcLoadOrder, 10) || nextLoadOrder;
    const baseOrder = parseInt(row.dataset.pcBaseOrder, 10) || loadOrder;
    return {
      row,
      cells,
      searchText,
      status,
      loadOrder,
      baseOrder,
      sortCache: Object.create(null),
    };
  }

  function refreshRowCacheText(scopeRows) {
    if (!scopeRows) {
      rowCache = rowCache.map((entry) => buildRowEntry(entry.row));
      return;
    }
    const rows = new Set($(scopeRows).toArray());
    rowCache = rowCache.map((entry) => rows.has(entry.row) ? buildRowEntry(entry.row) : entry);
  }

  function reloadReviewMetricColumns(nextDims) {
    const allowed = new Set(reviewMetricOptions.map((metric) => metric.key));
    const unique = [];
    nextDims.forEach((key) => {
      if (allowed.has(key) && !unique.includes(key)) unique.push(key);
    });
    if (!unique.length) return;
    const reloadAllRecords = hasCompleteLocalDataset();
    reviewDims = unique;
    currentSortColumn = null;
    currentSortAscending = true;
    columnFilters = [];
    syncReviewMetricHeaders();
    resetLoadedRowsForQuery({
      forceServer: true,
      fetchAll: reloadAllRecords,
      holdProgress: reloadAllRecords,
      status: reloadAllRecords ? 'Reloading full records...' : 'Searching...',
    });
  }

  function reloadPaperColumns(nextDims) {
    const allowed = new Set(paperColumnOptions.map((column) => column.key));
    const unique = [];
    nextDims.forEach((key) => {
      if (allowed.has(key) && !unique.includes(key)) unique.push(key);
    });
    if (!unique.length) return;
    const reloadAllRecords = hasCompleteLocalDataset();
    paperDims = unique;
    currentSortColumn = null;
    currentSortAscending = true;
    columnFilters = [];
    syncPaperColumnHeaders();
    $table.find('thead input.pc-th-search').val('');
    $table.find('thead .pc-th-filter-choice').prop('checked', false);
    updateMultiFilterSummaries($table.find('thead'));
    resetLoadedRowsForQuery({
      forceServer: true,
      fetchAll: reloadAllRecords,
      holdProgress: reloadAllRecords,
      status: reloadAllRecords ? 'Reloading full records...' : 'Searching...',
    });
  }

  function removeReviewMetricColumn(key) {
    const index = reviewDims.indexOf(key);
    if (index < 0 || reviewDims.length <= 1) return;
    const colIndex = REVIEW_METRIC_START_COLUMN + index;
    reviewDims = reviewDims.filter((dim) => dim !== key);
    delete reviewMetricSearchByDim[key];
    if (currentSortColumn === colIndex) {
      currentSortColumn = null;
      currentSortAscending = true;
    } else if (currentSortColumn !== null && currentSortColumn > colIndex) {
      currentSortColumn -= 1;
    }
    columnFilters = [];
    allLoadedRows().each(function () {
      if (this.cells[colIndex]) this.deleteCell(colIndex);
    });
    syncReviewMetricHeaders();
    applyReviewMetricSearchChannel(allLoadedRows());
    refreshRowCacheText();
    applyFiltersNow({ keepLoading: isLoading });
  }

  function ensureTableSettingsGui() {
    if (tableSettingsGui || !(window.lil && window.lil.GUI)) return !!tableSettingsGui;
    const toolbar = document.querySelector('.pc-paper-table-toolbar');
    const settingsButton = document.getElementById('pc_table_settings_btn');
    if (!toolbar || !settingsButton) return false;

    tableSettingsState = {
      render: renderMode === 'all' ? 'Full Records' : 'Page by page',
      rows: String(pageSize),
      page: 'Page 1 / 1',
      previous() {
        if (pageIndex <= 0) return;
        pageIndex -= 1;
        renderCurrentPage();
      },
      next() {
        const totalPages = getTotalPages();
        if (pageIndex >= totalPages - 1) return;
        pageIndex += 1;
        renderCurrentPage();
      },
    };

    tableSettingsGui = new window.lil.GUI({ title: 'Table Settings', container: toolbar });
    if (tableSettingsGui.domElement.parentNode !== toolbar) {
      toolbar.appendChild(tableSettingsGui.domElement);
    }
    tableSettingsGui.domElement.id = 'pc_table_settings_gui';
    tableSettingsGui.domElement.classList.add('pc-paper-table-gui');
    tableSettingsGui.domElement.style.display = 'none';

    tableSettingsRenderController = tableSettingsGui.add(tableSettingsState, 'render', ['Full Records', 'Page by page']).name('Render').onChange((value) => {
      renderMode = value === 'Full Records' ? 'all' : 'paged';
      $(`input[name="pc_render_mode"][value="${renderMode}"]`).prop('checked', true);
      pageIndex = 0;
      renderCurrentPage();
    }).listen();
    tableSettingsRowsController = tableSettingsGui.add(tableSettingsState, 'rows', ['100', '250', '500']).name('Rows').onChange((value) => {
      pageSize = parseInt(value, 10) || 100;
      $('#pc_page_size').val(String(pageSize));
      pageIndex = 0;
      renderCurrentPage();
    }).listen();
    tableSettingsPageController = tableSettingsGui.add(tableSettingsState, 'page').name('Page').listen();
    if (tableSettingsPageController.domElement) {
      tableSettingsPageController.domElement.classList.add('pc-table-gui-readonly');
      const pageInput = tableSettingsPageController.domElement.querySelector('input');
      if (pageInput) pageInput.setAttribute('readonly', 'readonly');
    }
    tableSettingsGui.add(tableSettingsState, 'previous').name('Previous Page');
    tableSettingsGui.add(tableSettingsState, 'next').name('Next Page');

    const sourceRow = document.createElement('div');
    sourceRow.className = 'pc-table-gui-source';
    sourceRow.innerHTML = 'Data hosted on <a target="_blank" rel="noopener" href="https://github.com/papercopilot/paperlists">GitHub</a> · <a target="_blank" rel="noopener" href="https://github.com/papercopilot/paperlists/issues">update data</a>';
    tableSettingsGui.domElement.appendChild(sourceRow);

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'pc-table-gui-close';
    closeBtn.setAttribute('aria-label', 'Close table settings');
    closeBtn.title = 'Close table settings';
    closeBtn.textContent = '×';
    closeBtn.addEventListener('click', (event) => {
      event.stopPropagation();
      setTableSettingsOpen(false);
    });
    tableSettingsGui.domElement.appendChild(closeBtn);

    $('#pc_table_settings').prop('hidden', true).attr('aria-hidden', 'true');
    syncTableSettingsGui();
    return true;
  }

  function isTableSettingsOpen() {
    if (tableSettingsGui) return tableSettingsGui.domElement.style.display !== 'none';
    return !$('#pc_table_settings').prop('hidden');
  }

  function setTableSettingsOpen(open) {
    if (!tableSettingsGui && !$('#pc_table_settings_btn').length) return;
    if (tableSettingsGui) {
      tableSettingsGui.domElement.style.display = open ? '' : 'none';
      if (open) syncTableSettingsGui();
    } else {
      $('#pc_table_settings').prop('hidden', !open);
    }
    if (open) setTableHelpOpen(false);
    $('#pc_table_settings_btn')
      .attr('aria-expanded', open ? 'true' : 'false')
      .toggleClass('is-open', open);
  }

  function setTableHelpOpen(open) {
    $('#pc_table_help_panel').prop('hidden', !open);
    $('#pc_table_help_toggle').prop('checked', open);
    $('.pc-paper-table-help-toggle').toggleClass('is-open', open);
  }

  function updateTableGuiController(controller) {
    if (controller && typeof controller.updateDisplay === 'function') controller.updateDisplay();
  }

  function syncTableSettingsGui() {
    if (!tableSettingsState) return;
    const totalPages = getTotalPages();
    tableSettingsState.render = renderMode === 'all' ? 'Full Records' : 'Page by page';
    tableSettingsState.rows = String(pageSize);
    tableSettingsState.page = renderMode === 'all'
      ? `Full Records · ${formatCount(filteredEntries.length)} rows`
      : `Page ${formatCount(filteredEntries.length ? pageIndex + 1 : 1)} / ${formatCount(totalPages)}`;
    updateTableGuiController(tableSettingsRenderController);
    updateTableGuiController(tableSettingsRowsController);
    updateTableGuiController(tableSettingsPageController);
  }

  function bindControls() {
    $('#btn_fetchall').on('click', function () {
      isFetchAll = true;
      $(this).prop('disabled', true).text('Loading...');
      if (!isLoading) loadMoreRows();
    });

    $('#btn_order_reset').on('click', function () {
      resetOrder();
    });

    $table.find('thead').on('input search', 'input.pc-th-search', scheduleFilters);
    $table.find('thead').on('change', '.pc-th-filter-choice', function () {
      updateMultiFilterSummaries($(this).closest('.pc-th-multi'));
      scheduleFilters();
    });

    $('#pc_page_size').on('change', function () {
      const value = $(this).val();
      pageSize = parseInt(value, 10) || 100;
      pageIndex = 0;
      renderCurrentPage();
    });

    $('#pc_table_help_toggle').on('change', function (event) {
      event.stopPropagation();
      setTableHelpOpen(this.checked);
      if (this.checked) setTableSettingsOpen(false);
    });

    $('#pc_table_settings_btn').on('click', function (event) {
      event.stopPropagation();
      ensureTableSettingsGui();
      setTableSettingsOpen(!isTableSettingsOpen());
    });

    $(document).on('click', '#pc_table_settings, #pc_table_settings_gui, .pc-paper-table-help-wrap', function (event) {
      event.stopPropagation();
    });

    $(document).on('click', function () {
      setTableSettingsOpen(false);
      setTableHelpOpen(false);
    });

    $(document).on('click', '.pc-review-metric-add .pc-review-metric-menu-btn', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const key = String($(this).data('metricKey') || '');
      if (!key || reviewDims.includes(key)) return;
      $(this).closest('details').prop('open', false);
      reloadReviewMetricColumns(reviewDims.concat(key));
    });

    $(document).on('click', '.pc-review-metric-switch .pc-review-metric-menu-btn', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const key = String($(this).data('metricKey') || '');
      const index = parseInt($(this).closest('.pc-review-metric-switch').data('metricIndex'), 10);
      if (!key || Number.isNaN(index) || reviewDims[index] === key) return;
      const nextDims = reviewDims.slice();
      const existingIndex = nextDims.indexOf(key);
      if (existingIndex >= 0) {
        nextDims[existingIndex] = nextDims[index];
      }
      nextDims[index] = key;
      $(this).closest('details').prop('open', false);
      reloadReviewMetricColumns(nextDims);
    });

    $(document).on('click', '.pc-review-metric-remove', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const key = String($(this).data('metricDim') || '');
      if (!key || reviewDims.length <= 1) return;
      removeReviewMetricColumn(key);
    });

    $(document).on('click', '.pc-paper-column-add .pc-paper-column-menu-btn', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const key = String($(this).data('paperColumnKey') || '');
      if (!key || paperDims.includes(key)) return;
      $(this).closest('details').prop('open', false);
      reloadPaperColumns(paperDims.concat(key));
    });

    $(document).on('click', '.pc-paper-column-switch .pc-paper-column-menu-btn', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const key = String($(this).data('paperColumnKey') || '');
      const index = parseInt($(this).closest('.pc-paper-column-switch').data('paperColumnIndex'), 10);
      if (!key || Number.isNaN(index) || paperDims[index] === key) return;
      const nextDims = paperDims.slice();
      const existingIndex = nextDims.indexOf(key);
      if (existingIndex >= 0) {
        nextDims[existingIndex] = nextDims[index];
      }
      nextDims[index] = key;
      $(this).closest('details').prop('open', false);
      reloadPaperColumns(nextDims);
    });

    $(document).on('click', '.pc-paper-column-remove', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const key = String($(this).data('paperColumnKey') || '');
      if (!key || paperDims.length <= 1) return;
      reloadPaperColumns(paperDims.filter((dim) => dim !== key));
    });

    $(document).on('click', '.pc-review-metric-channel', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const metricDim = String($(this).data('metricDim') || '');
      if (!metricDim) return;
      const value = $(this).data('channel');
      const nextMetricSearch = ['raw', 'std', 'mean', 'min', 'max'].includes(value) ? value : 'raw';
      if (nextMetricSearch === reviewMetricChannelFor(metricDim)) return;
      columnFilters = readColumnFilters();
      const metricColIndex = reviewMetricColumnIndex(metricDim);
      const hasActiveMetricFilter = metricColIndex >= 0 && columnFilters.some((filter) => filter.colIndex === metricColIndex);
      reviewMetricSearchByDim[metricDim] = nextMetricSearch;
      syncReviewMetricHeaders();
      columnFilters = readColumnFilters();
      applyReviewMetricSearchChannel(renderedDataRows());
      if (currentSortColumn === metricColIndex) applyCurrentSort();
      if (hasActiveMetricFilter) {
        resetLoadedRowsForQuery();
      } else {
        applyFiltersNow({ keepLoading: isLoading });
      }
    });

    $('input[name="pc_render_mode"]').on('change', function () {
      renderMode = $(this).val() === 'all' ? 'all' : 'paged';
      pageIndex = 0;
      renderCurrentPage();
    });

    $('#pc_prev_page').on('click', function () {
      if (pageIndex > 0) {
        pageIndex -= 1;
        renderCurrentPage();
      }
    });

    $('#pc_next_page').on('click', function () {
      const totalPages = getTotalPages();
      if (pageIndex < totalPages - 1) {
        pageIndex += 1;
        renderCurrentPage();
      }
    });

    $(document).on('click', '.sort-btn', function (event) {
      event.preventDefault();
      const colIndex = parseInt($(this).data('col'), 10);
      if (Number.isNaN(colIndex)) return;

      if (currentSortColumn === colIndex) {
        currentSortAscending = !currentSortAscending;
      } else {
        currentSortColumn = colIndex;
        currentSortAscending = true;
      }

      sortTable(colIndex, currentSortAscending);
      syncSortButtons();
    });

    $('#aff_switch').on('change', function () {
      updateAffiliationCells(allLoadedRows());
      refreshRowCacheText();
      applyFiltersNow();
    });

    $('#metrics_switch').on('change', function () {
      updateMetricsCells(allLoadedRows());
      refreshRowCacheText();
      applyFiltersNow();
    });

    $('#rating_avg_switch').on('change', function () {
      updateRatingCells(allLoadedRows());
      refreshRowCacheText();
      applyFiltersNow();
    });

    $('#confidence_avg_switch').on('change', function () {
      updateConfidenceCells(allLoadedRows());
      refreshRowCacheText();
      applyFiltersNow();
    });
  }

  function allLoadedRows() {
    return $(rowCache.map((entry) => entry.row));
  }

  function renderedDataRows() {
    return $tbody.children('tr').not('.pc-virtual-spacer');
  }

  function scheduleFilters() {
    window.clearTimeout(filterTimer);
    pageIndex = 0;
    columnFilters = readColumnFilters();
    const localFilterOnly = hasCompleteLocalDataset();
    filterTimer = window.setTimeout(function () {
      if (localFilterOnly && hasCompleteLocalDataset()) {
        applyFiltersNow({ useColumnFilters: true });
      } else {
        resetLoadedRowsForQuery();
      }
    }, localFilterOnly ? Math.max(60, Math.floor(FILTER_DELAY / 2)) : FILTER_DELAY);
  }

  function resetLoadedRowsForQuery(options) {
    const forceServer = options && options.forceServer === true;
    if (!forceServer && hasCompleteLocalDataset()) {
      pendingQueryReplace = false;
      applyFiltersNow({ useColumnFilters: true });
      return;
    }
    const fetchAllAfterReset = (options && options.fetchAll === true) || hasActiveColumnFilters();
    const holdProgress = options && options.holdProgress === true;
    const statusText = options && options.status;
    progressRecordHold = holdProgress ? currentProgressRecordCount() : null;
    updateProgressReloadState(fullTotalRecords || totalRecords);
    loadGeneration += 1;
    fullDatasetLoaded = false;
    if (currentRequest) {
      currentRequest.abort();
      currentRequest = null;
    }
    isLoading = false;
    isFetchAll = fetchAllAfterReset;
    pendingQueryReplace = rowCache.length > 0 || $tbody.children().length > 0;
    batch = 0;
    nRecords = 0;
    totalRecords = null;
    pageIndex = 0;
    applyReviewMetricSearchChannel(renderedDataRows());
    if (rowCache.length && !isFetchAll) {
      applyFiltersNow({ useColumnFilters: true, keepLoading: true });
    }
    setTableLoading($tbody.children().length > 0);
    $('#btn_fetchall').prop('disabled', isFetchAll).text(isFetchAll ? 'Loading...' : 'Fetch all');
    updateLoadStatus(statusText || (isFetchAll ? 'Searching all matches...' : 'Searching...'));
    loadMoreRows();
  }

  function readColumnFilters() {
    const filters = [];
    $table.find('thead input.pc-th-search').each(function () {
      const colIndex = parseInt($(this).data('col'), 10);
      if (Number.isNaN(colIndex)) return;
      const terms = parseSearchTerms($(this).val());
      if (terms.length) filters.push({ colIndex, terms });
    });
    $table.find('thead .pc-th-multi').each(function () {
      const colIndex = parseInt($(this).data('col'), 10);
      if (Number.isNaN(colIndex)) return;
      const terms = $(this).find('.pc-th-filter-choice:checked').map(function () {
        return cleanText($(this).val()).toLowerCase();
      }).get().filter(Boolean);
      if (terms.length) filters.push({ colIndex, terms, match: 'any' });
    });
    return filters;
  }

  function parseSearchTerms(query) {
    const terms = [];
    const pattern = /"([^"]+)"|'([^']+)'|(\S+)/g;
    let match;
    while ((match = pattern.exec(String(query || ''))) !== null) {
      const term = cleanText(match[1] || match[2] || match[3]).toLowerCase();
      if (term) terms.push(term);
    }
    return terms;
  }

  function applyFiltersNow(options) {
    const opts = options || {};
    const useColumnFilters = opts.useColumnFilters === true ||
      (opts.useColumnFilters !== false && hasCompleteLocalDataset() && columnFilters.length > 0);
    const keepLoading = opts.keepLoading === true;
    if (filterFrame) window.cancelAnimationFrame(filterFrame);
    filterFrame = window.requestAnimationFrame(function () {
      if (!useColumnFilters) {
        filteredEntries = rowCache.slice();
        pageIndex = Math.min(pageIndex, Math.max(0, getTotalPages() - 1));
        updateRecordStats();
        renderCurrentPage({ keepLoading });
        return;
      }

      const nextFilteredEntries = [];

      rowCache.forEach((entry) => {
        let showRow = true;

        if (showRow && useColumnFilters) {
          for (let i = 0; i < columnFilters.length; i += 1) {
            const filter = columnFilters[i];
            const cellText = entryCellSearchText(entry, filter.colIndex);
            if (filter.match === 'any') {
              const hasMatch = filter.terms.some((term) => cellText.includes(term));
              if (!hasMatch) {
                showRow = false;
              }
            } else {
              for (let j = 0; j < filter.terms.length; j += 1) {
                if (!cellText.includes(filter.terms[j])) {
                  showRow = false;
                  break;
                }
              }
            }
            if (!showRow) break;
          }
        }

        if (showRow) nextFilteredEntries.push(entry);
      });

      filteredEntries = nextFilteredEntries;
      pageIndex = Math.min(pageIndex, Math.max(0, getTotalPages() - 1));
      updateRecordStats();
      renderCurrentPage({ keepLoading });
    });
  }

  function shouldVirtualizeGiantTable(total) {
    const count = Number.isFinite(Number(total)) ? Number(total) : filteredEntries.length;
    return renderMode === 'all' && count > VIRTUAL_TABLE_MIN_ROWS;
  }

  function getEffectivePageSize(total) {
    const count = Number.isFinite(Number(total)) ? Number(total) : filteredEntries.length;
    if (renderMode === 'all') return Math.max(count, 1);
    return pageSize === 'all' ? Math.max(filteredEntries.length, 1) : pageSize;
  }

  function getTotalPages() {
    const effectiveSize = getEffectivePageSize();
    return Math.max(1, Math.ceil(filteredEntries.length / effectiveSize));
  }

  function clearRenderedRows() {
    while ($tbody[0].firstChild) {
      $tbody[0].removeChild($tbody[0].firstChild);
    }
  }

  function tableColumnCount() {
    const headerCells = $table.find('thead tr').last().children('th').length;
    if (headerCells) return headerCells;
    const cachedRow = rowCache.find((entry) => entry.row && entry.row.cells && entry.row.cells.length);
    return cachedRow ? cachedRow.row.cells.length : 1;
  }

  function buildVirtualSpacerRow(height, className) {
    const tr = document.createElement('tr');
    tr.className = `pc-virtual-spacer ${className || ''}`;
    tr.setAttribute('aria-hidden', 'true');
    const td = document.createElement('td');
    const pxHeight = `${Math.max(0, Math.round(height))}px`;
    td.colSpan = tableColumnCount();
    tr.style.height = pxHeight;
    td.style.height = pxHeight;
    tr.appendChild(td);
    return tr;
  }

  function tableHasOwnVerticalScroll() {
    const frame = $tableFrame[0];
    if (!frame) return false;
    const style = window.getComputedStyle(frame);
    const overflowY = style.overflowY || style.overflow;
    return frame.scrollHeight > frame.clientHeight + 2 && overflowY !== 'visible' && overflowY !== 'clip';
  }

  function virtualViewportBounds() {
    const frame = $tableFrame[0];
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight || 800;
    if (tableHasOwnVerticalScroll() && frame) {
      const rect = frame.getBoundingClientRect();
      return {
        top: Math.max(0, rect.top),
        bottom: Math.min(viewportHeight, rect.bottom),
      };
    }
    return { top: 0, bottom: viewportHeight };
  }

  function virtualVisibleRange(totalMatches) {
    const bodyRect = $tbody[0].getBoundingClientRect();
    const bounds = virtualViewportBounds();
    const visibleHeight = Math.max(virtualRowHeight, bounds.bottom - bounds.top);
    const firstVisible = Math.floor((bounds.top - bodyRect.top) / virtualRowHeight);
    const maxStart = Math.max(0, totalMatches - 1);
    const start = Math.max(0, Math.min(maxStart, firstVisible - VIRTUAL_OVERSCAN_ROWS));
    const count = Math.ceil(visibleHeight / virtualRowHeight) + (VIRTUAL_OVERSCAN_ROWS * 2);
    const end = Math.max(start, Math.min(totalMatches, start + count));
    return { start, end };
  }

  function updateVirtualRowHeight(rows) {
    const measured = rows
      .map((row) => row.getBoundingClientRect().height)
      .filter((height) => Number.isFinite(height) && height > 0);
    if (!measured.length) return;
    const average = measured.reduce((sum, height) => sum + height, 0) / measured.length;
    if (average < 18 || average > 180) return;
    virtualRowHeight = (virtualRowHeight * 0.7) + (average * 0.3);
  }

  function bindVirtualTableScroll() {
    $(window)
      .off('.pcPaperlistVirtual')
      .on('scroll.pcPaperlistVirtual resize.pcPaperlistVirtual', scheduleVirtualTableRender);
    $tableFrame
      .off('.pcPaperlistVirtual')
      .on('scroll.pcPaperlistVirtual', scheduleVirtualTableRender);
  }

  function disableVirtualTable() {
    if (!virtualTableActive) return;
    virtualTableActive = false;
    virtualStartIndex = 0;
    virtualEndIndex = 0;
    if (virtualFrame) {
      window.cancelAnimationFrame(virtualFrame);
      virtualFrame = null;
    }
    $(window).off('.pcPaperlistVirtual');
    $tableFrame.off('.pcPaperlistVirtual');
    $table.removeClass('pc-paper-table-virtual');
  }

  function scheduleVirtualTableRender() {
    if (!virtualTableActive) return;
    if (virtualFrame) window.cancelAnimationFrame(virtualFrame);
    virtualFrame = window.requestAnimationFrame(function () {
      virtualFrame = null;
      renderVirtualTableRows();
    });
  }

  function renderVirtualTableRows() {
    if (!virtualTableActive) return;
    const totalMatches = filteredEntries.length;
    if (!totalMatches) {
      clearRenderedRows();
      return;
    }

    const range = virtualVisibleRange(totalMatches);
    const rangeUnchanged = range.start === virtualStartIndex &&
      range.end === virtualEndIndex &&
      $tbody.children('tr').length > 0;
    if (rangeUnchanged) return;

    virtualStartIndex = range.start;
    virtualEndIndex = range.end;
    const pageEntries = filteredEntries.slice(range.start, range.end);
    const rows = pageEntries.map((entry) => entry.row);
    const frag = document.createDocumentFragment();
    const topHeight = range.start * virtualRowHeight;
    const bottomHeight = Math.max(0, (totalMatches - range.end) * virtualRowHeight);

    frag.appendChild(buildVirtualSpacerRow(topHeight, 'pc-virtual-spacer-top'));
    pageEntries.forEach((entry, index) => {
      renderIndexCell(entry, range.start + index + 1);
      entry.row.style.display = '';
      frag.appendChild(entry.row);
    });
    frag.appendChild(buildVirtualSpacerRow(bottomHeight, 'pc-virtual-spacer-bottom'));

    clearRenderedRows();
    $tbody[0].appendChild(frag);
    applyReviewMetricSearchChannel($(rows));
    applySearchHighlights(rows);
    updateVirtualRowHeight(rows);

    $('#pc_visible_range').text(`${formatCount(range.start + 1)}-${formatCount(range.end)} of ${formatCount(totalMatches)} matching loaded rows`);
  }

  function renderVirtualTable(options) {
    const opts = options || {};
    virtualTableActive = true;
    virtualStartIndex = -1;
    virtualEndIndex = -1;
    $table.addClass('pc-paper-table-virtual');
    bindVirtualTableScroll();
    renderVirtualTableRows();
    if (!opts.keepLoading) setTableLoading(false);

    $('#pc_page_state').text(`Full Records · ${formatCount(filteredEntries.length)} rows`);
    $('#pc_page_size').prop('disabled', true);
    $('#pc_prev_page').prop('disabled', true);
    $('#pc_next_page').prop('disabled', true);
    syncTableSettingsGui();
  }

  function renderIndexCell(entry, currentRank) {
    const indexCell = entry && entry.row ? entry.row.cells[0] : null;
    if (!indexCell) return;
    const baseRank = entry.baseOrder || currentRank;
    if (currentSortColumn !== null || hasActiveColumnFilters()) {
      indexCell.innerHTML = `<small class="pc-row-index" title="Default order ${formatCount(baseRank)}; current row ${formatCount(currentRank)}"><span class="pc-row-base">${formatCount(baseRank)}</span><span class="pc-row-current">#${formatCount(currentRank)}</span></small>`;
    } else {
      indexCell.innerHTML = `<small class="pc-row-index" title="Default order ${formatCount(baseRank)}"><span class="pc-row-base">${formatCount(baseRank)}</span></small>`;
    }
  }

  function renderCurrentPage(options) {
    const opts = options || {};
    const totalMatches = filteredEntries.length;
    if (shouldVirtualizeGiantTable(totalMatches)) {
      renderVirtualTable(opts);
      return;
    }

    disableVirtualTable();
    const effectiveSize = getEffectivePageSize(totalMatches);
    const totalPages = getTotalPages();
    pageIndex = Math.min(pageIndex, totalPages - 1);

    const start = totalMatches ? pageIndex * effectiveSize : 0;
    const end = Math.min(totalMatches, start + effectiveSize);
    const pageEntries = filteredEntries.slice(start, end);
    const frag = document.createDocumentFragment();
    const rows = pageEntries.map((entry) => entry.row);

    pageEntries.forEach((entry, index) => {
      renderIndexCell(entry, start + index + 1);
      entry.row.style.display = '';
      frag.appendChild(entry.row);
    });

    clearRenderedRows();
    $tbody[0].appendChild(frag);
    applyReviewMetricSearchChannel($(rows));
    if (pageEntries.length <= HIGHLIGHT_ROW_LIMIT) {
      applySearchHighlights(rows);
    } else if (columnFilters.length) {
      clearSearchHighlights($(rows));
    }
    if (!opts.keepLoading) setTableLoading(false);

    $('#pc_visible_range').text(totalMatches
      ? `${formatCount(start + 1)}-${formatCount(end)} of ${formatCount(totalMatches)} matching loaded rows`
      : '0 matching loaded rows');
    const canPage = renderMode !== 'all' && totalPages > 1;
    $('#pc_page_state').text(renderMode === 'all'
      ? 'Full Records'
      : `Page ${formatCount(totalMatches ? pageIndex + 1 : 1)} / ${formatCount(totalPages)}`);
    $('#pc_page_size').prop('disabled', renderMode === 'all');
    $('#pc_prev_page').prop('disabled', !canPage || pageIndex <= 0);
    $('#pc_next_page').prop('disabled', !canPage || pageIndex >= totalPages - 1);
    syncTableSettingsGui();
  }

  function escapeRegExp(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function uniqueTerms(terms) {
    return Array.from(new Set((terms || [])
      .map((term) => cleanText(term).toLowerCase())
      .filter(Boolean)))
      .sort((a, b) => b.length - a.length);
  }

  function clearSearchHighlights($scope) {
    $scope.find('mark.pc-search-hit').each(function () {
      const mark = this;
      const parent = mark.parentNode;
      if (!parent) return;
      while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
      parent.removeChild(mark);
      parent.normalize();
    });
  }

  function applySearchHighlights(rows) {
    const $rows = $(rows || []);
    if (!$rows.length) return;
    clearSearchHighlights($rows);

    columnFilters.forEach((filter) => {
      const terms = uniqueTerms(filter.terms);
      if (!terms.length) return;
      const matcher = new RegExp(terms.map(escapeRegExp).join('|'), 'gi');

      $rows.each(function () {
        const cell = this.cells[filter.colIndex];
        if (cell) highlightTextMatches(cell, matcher);
      });
    });
  }

  function highlightTextMatches(root, matcher) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const value = node.nodeValue || '';
        if (!value.trim()) return NodeFilter.FILTER_REJECT;
        const parent = node.parentNode;
        if (!parent || parent.nodeType !== 1) return NodeFilter.FILTER_REJECT;
        if (parent.closest('mark.pc-search-hit, script, style, textarea, input, select, option')) {
          return NodeFilter.FILTER_REJECT;
        }
        matcher.lastIndex = 0;
        return matcher.test(value) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      },
    });

    const nodes = [];
    let node = walker.nextNode();
    while (node) {
      nodes.push(node);
      node = walker.nextNode();
    }

    nodes.forEach((textNode) => {
      const value = textNode.nodeValue || '';
      const frag = document.createDocumentFragment();
      let cursor = 0;
      matcher.lastIndex = 0;
      value.replace(matcher, (match, offset) => {
        if (offset > cursor) frag.appendChild(document.createTextNode(value.slice(cursor, offset)));
        const mark = document.createElement('mark');
        mark.className = 'pc-search-hit';
        mark.textContent = match;
        frag.appendChild(mark);
        cursor = offset + match.length;
        return match;
      });
      if (cursor < value.length) frag.appendChild(document.createTextNode(value.slice(cursor)));
      textNode.parentNode.replaceChild(frag, textNode);
    });
  }

  function applyActiveDisplayModes($scope) {
    updateAffiliationCells($scope);
    updateMetricsCells($scope);
    updateRatingCells($scope);
    updateConfidenceCells($scope);
  }

  function applyReviewMetricSearchChannel($scope) {
    if (!isReviewMetricTable() || !$scope || !$scope.length) return;
    $scope.find('.pc-review-metric-cell').each(function () {
      const $cell = $(this);
      const channel = reviewMetricChannelFor(String($cell.attr('data-metric-dim') || ''));
      const value = $cell.attr(`data-search-${channel}`) || '';
      this.dataset.search = value;
      this.dataset.sort = $cell.attr(`data-sort-${channel}`) || value;
      $cell.find('.pc-review-metric-value').prop('hidden', true);
      $cell.find(`.pc-review-metric-value-${channel}`).prop('hidden', false);
    });
  }

  function updateAffiliationCells($scope) {
    const $switch = $('#aff_switch');
    if (!$switch.length) return;
    const mode = $switch.val();
    $scope.find('.aff-link').each(function () {
      const $cell = $(this);
      const dep = $cell.data('dep');
      const campus = $cell.data('campus');
      const norm = $cell.data('norm');
      const abbr = $cell.data('abbr');
      const url = $cell.data('url');

      let text = norm;
      if (mode === 'dep' && (dep || campus)) {
        text = `${dep ? `<span style="color:#555;font-style:italic;">${dep}</span>, ` : ''}` +
          `${campus ? `<span style="color:#999;">${campus}</span>, ` : ''}` +
          norm;
      } else if (mode === 'abbr') {
        text = abbr || norm;
      }

      $cell.html(url ? `<a href="${url}" target="_blank" rel="noopener">${text}</a>` : text);
    });
  }

  function updateMetricsCells($scope) {
    const $switch = $('#metrics_switch');
    if (!$switch.length) return;
    const mode = $switch.val();
    $scope.find('.metrics-cell').each(function () {
      const $cell = $(this);
      if (mode === 'gs' || mode === 'rating_avg' || mode === 'rating_str') {
        const html = $cell.data(mode);
        $cell.html(html == null ? '' : html);
      } else {
        const val = $cell.data(mode);
        $cell.text(val == null ? '' : val);
      }
    });
  }

  function updateRatingCells($scope) {
    const $switch = $('#rating_avg_switch');
    if (!$switch.length) return;
    const mode = $switch.val();
    $scope.find('.rating-cell').each(function () {
      const $cell = $(this);
      if (mode === 'all') {
        const html = $cell.attr('data-all');
        $cell.html(html == null ? '' : html);
      } else {
        const val = $cell.data(mode);
        $cell.text(val == null ? '' : val);
      }
    });
  }

  function updateConfidenceCells($scope) {
    const $switch = $('#confidence_avg_switch');
    if (!$switch.length) return;
    const mode = $switch.val();
    $scope.find('.confidence-cell').each(function () {
      const $cell = $(this);
      if (mode === 'all') {
        const html = $cell.attr('data-all');
        $cell.html(html == null ? '' : html);
      } else {
        const val = $cell.data(mode);
        $cell.text(val == null ? '' : val);
      }
    });
  }

  function syncSortButtons() {
    $('.sort-btn').each(function () {
      const idx = parseInt($(this).data('col'), 10);
      const isCurrent = idx === currentSortColumn;
      const direction = currentSortAscending ? 'A-Z' : 'Z-A';
      const headerLabel = cleanText($(this).data('sortName') || $(this).closest('th').clone().find('.sort-btn').remove().end().text());
      $(this)
        .toggleClass('pc-sort-active', isCurrent)
        .toggleClass('pc-sort-asc', isCurrent && currentSortAscending)
        .toggleClass('pc-sort-desc', isCurrent && !currentSortAscending)
        .attr('aria-label', isCurrent ? `${headerLabel} sorted ${direction}. Click to reverse.` : `Sort ${headerLabel}`)
        .attr('title', isCurrent ? `${headerLabel} sorted ${direction}. Click to reverse.` : `Sort ${headerLabel}`);
      $(this).closest('th').attr('aria-sort', isCurrent ? (currentSortAscending ? 'ascending' : 'descending') : 'none');
    });
  }

  function resetOrder() {
    if (!rowCache.length) return;
    currentSortColumn = null;
    currentSortAscending = true;
    applyDefaultOrder();
    syncSortButtons();
    pageIndex = 0;
    applyFiltersNow();
  }

  function sortTable(colIndex, ascending) {
    if (!rowCache.length) return;
    currentSortColumn = colIndex;
    currentSortAscending = ascending;
    applyCurrentSort();
    pageIndex = 0;
    applyFiltersNow();
  }

  function applyActiveOrder() {
    if (currentSortColumn === null) {
      applyDefaultOrder();
    } else {
      updateDefaultOrderRanks();
      applyCurrentSort();
    }
  }

  function buildSortKey(rawValue) {
    const raw = cleanText(rawValue);
    const numericParts = raw.split('|').map((part) => cleanText(part).replace(/,/g, ''));
    return {
      raw,
      numericParts,
      isNumeric: numericParts.every((part) => part === '' || !Number.isNaN(Number(part))),
    };
  }

  function reviewMetricColumnIndex(metricDim) {
    if (!isReviewMetricTable()) return -1;
    const metricIndex = reviewDims.indexOf(metricDim);
    return metricIndex >= 0 ? REVIEW_METRIC_START_COLUMN + metricIndex : -1;
  }

  function reviewMetricDimForColumn(colIndex) {
    if (!isReviewMetricTable()) return '';
    const metricIndex = colIndex - REVIEW_METRIC_START_COLUMN;
    return metricIndex >= 0 && metricIndex < reviewDims.length ? reviewDims[metricIndex] : '';
  }

  function reviewMetricChannelValue(cell, channel, attrPrefix) {
    if (!cell) return '';
    const value = cell.getAttribute(`data-${attrPrefix}-${channel}`);
    return value == null ? '' : value;
  }

  function entryCellSearchText(entry, colIndex) {
    const metricDim = reviewMetricDimForColumn(colIndex);
    if (!metricDim) return entry.cells[colIndex] || '';
    const cell = entry.row.cells[colIndex];
    const channel = reviewMetricChannelFor(metricDim);
    return cleanText(reviewMetricChannelValue(cell, channel, 'search')).toLowerCase();
  }

  function metricSortNumber(entry, colIndex, channel) {
    const cell = entry.row.cells[colIndex];
    const value = cleanText(reviewMetricChannelValue(cell, channel, 'sort'));
    if (!value) return null;
    const number = Number(value.replace(/,/g, ''));
    return Number.isFinite(number) ? number : null;
  }

  function compareNumbers(aValue, bValue, descending) {
    const aMissing = aValue === null || aValue === undefined;
    const bMissing = bValue === null || bValue === undefined;
    if (aMissing && bMissing) return 0;
    if (aMissing) return 1;
    if (bMissing) return -1;
    if (aValue === bValue) return 0;
    return descending ? bValue - aValue : aValue - bValue;
  }

  function defaultOrderComparator(a, b) {
    const ratingCol = reviewMetricColumnIndex('rating');
    if (ratingCol >= 0) {
      const meanCompare = compareNumbers(metricSortNumber(a, ratingCol, 'mean'), metricSortNumber(b, ratingCol, 'mean'), true);
      if (meanCompare !== 0) return meanCompare;
      const stdCompare = compareNumbers(metricSortNumber(a, ratingCol, 'std'), metricSortNumber(b, ratingCol, 'std'), false);
      if (stdCompare !== 0) return stdCompare;
    }
    return (a.loadOrder || 0) - (b.loadOrder || 0);
  }

  function updateDefaultOrderRanks() {
    rowCache.slice().sort(defaultOrderComparator).forEach((entry, index) => {
      entry.baseOrder = index + 1;
      entry.row.dataset.pcBaseOrder = String(entry.baseOrder);
    });
  }

  function applyDefaultOrder() {
    rowCache.sort(defaultOrderComparator);
    rowCache.forEach((entry, index) => {
      entry.baseOrder = index + 1;
      entry.row.dataset.pcBaseOrder = String(entry.baseOrder);
    });
  }

  function sortKeyForEntry(entry, colIndex) {
    const metricDim = reviewMetricDimForColumn(colIndex);
    const channel = metricDim ? reviewMetricChannelFor(metricDim) : '';
    const cacheKey = metricDim ? `${colIndex}:${channel}` : String(colIndex);
    if (entry.sortCache && entry.sortCache[cacheKey]) return entry.sortCache[cacheKey];
    const cell = entry.row.cells[colIndex];
    const raw = metricDim
      ? cleanText(reviewMetricChannelValue(cell, channel, 'sort') || reviewMetricChannelValue(cell, channel, 'search'))
      : cleanText(cell ? cell.dataset.sort || cell.dataset.val || cell.textContent : '');
    const key = buildSortKey(raw);
    if (!entry.sortCache) entry.sortCache = Object.create(null);
    entry.sortCache[cacheKey] = key;
    return key;
  }

  function applyCurrentSort() {
    if (currentSortColumn === null || !rowCache.length) return;
    const colIndex = currentSortColumn;
    const keyedRows = rowCache.map((entry) => ({
      entry,
      key: sortKeyForEntry(entry, colIndex),
    }));
    const numeric = keyedRows.every((item) => item.key.isNumeric);

    keyedRows.sort((a, b) => {
      const keyA = a.key;
      const keyB = b.key;
      if (numeric) {
        const aParts = keyA.numericParts;
        const bParts = keyB.numericParts;
        const len = Math.max(aParts.length, bParts.length);
        for (let i = 0; i < len; i += 1) {
          const aNumber = aParts[i] === '' || aParts[i] === undefined ? Number.NEGATIVE_INFINITY : Number(aParts[i]);
          const bNumber = bParts[i] === '' || bParts[i] === undefined ? Number.NEGATIVE_INFINITY : Number(bParts[i]);
          if (aNumber !== bNumber) {
            return currentSortAscending ? aNumber - bNumber : bNumber - aNumber;
          }
        }
        return 0;
      }
      return currentSortAscending ? keyA.raw.localeCompare(keyB.raw) : keyB.raw.localeCompare(keyA.raw);
    });

    rowCache = keyedRows.map((item) => item.entry);
  }

  function autoColor(name) {
    let hash = 0;
    const key = String(name || '');
    for (let i = 0; i < key.length; i += 1) {
      hash = key.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = Math.abs(hash) % 360;
    return `hsla(${hue},70%,85%,${HIGHLIGHT_ALPHA})`;
  }

  function hexToRgba(hex, alpha = HIGHLIGHT_ALPHA) {
    let clean = String(hex || '').replace('#', '');
    if (clean.length === 3) clean = clean.split('').map((c) => c + c).join('');
    const int = parseInt(clean, 16);
    const r = (int >> 16) & 255;
    const g = (int >> 8) & 255;
    const b = int & 255;
    return `rgba(${r},${g},${b},${alpha})`;
  }

  function countryToColor(country) {
    const key = cleanText(country).toLowerCase();
    const base = COUNTRY_COLOR_MAP[key];
    return base ? hexToRgba(base) : autoColor(key);
  }

  function bindHoverHighlighting() {
    function colourize($el, colour) {
      $el.css({
        'background-color': colour,
        transition: 'background-color 0.12s',
      }).attr('data-coloured', '1');
    }

    function clearHighlights($row) {
      $row.find('[data-coloured="1"]').removeAttr('style data-coloured');
    }

    function splitData($el, key) {
      return String($el.data(key) || '').split('+').filter(Boolean);
    }

    function matchAny($row, selector, dataKey, values, colour) {
      values.forEach((val) => {
        $row.find(`${selector}[data-${dataKey}*="${val}"]`).each(function () {
          const targetVals = String($(this).data(dataKey) || '').split('+');
          if (targetVals.includes(val)) colourize($(this), colour);
        });
      });
    }

    $(document)
      .off('.pcPaperlistHover')
      .on('mouseenter.pcPaperlistHover', '.author-link', function () {
        const $row = $(this).closest('tr');
        const affs = splitData($(this), 'aff');
        const countries = splitData($(this), 'country');
        const fill = countryToColor(countries[0] || '');
        matchAny($row, '.aff-link', 'aff', affs, fill);
        matchAny($row, '.country-link', 'index', countries, fill);
        colourize($(this), fill);
      })
      .on('mouseleave.pcPaperlistHover', '.author-link', function () {
        clearHighlights($(this).closest('tr'));
      })
      .on('mouseenter.pcPaperlistHover', '.aff-link', function () {
        const $row = $(this).closest('tr');
        const affs = splitData($(this), 'aff');
        const countries = splitData($(this), 'country');
        const fill = countryToColor(countries[0] || '');
        matchAny($row, '.author-link', 'aff', affs, fill);
        matchAny($row, '.country-link', 'index', countries, fill);
        colourize($(this), fill);
      })
      .on('mouseleave.pcPaperlistHover', '.aff-link', function () {
        clearHighlights($(this).closest('tr'));
      })
      .on('mouseenter.pcPaperlistHover', '.country-link', function () {
        const $row = $(this).closest('tr');
        const idx = String($(this).data('index') || '');
        const name = cleanText($(this).text());
        const fill = countryToColor(name);
        matchAny($row, '.author-link', 'country', [idx], fill);
        matchAny($row, '.aff-link', 'country', [idx], fill);
        colourize($(this), fill);
      })
      .on('mouseleave.pcPaperlistHover', '.country-link', function () {
        clearHighlights($(this).closest('tr'));
      });
  }

  function bindAuthorPopup() {
    let hidePopupTimer = null;

    function movePopup(e) {
      $('#author-popup').css({
        top: `${e.pageY + 14}px`,
        left: `${e.pageX + 14}px`,
      });
    }

    $(document)
      .off('.pcPaperlistAuthorPopup')
      .on('mouseenter.pcPaperlistAuthorPopup', '.author-link', function (e) {
        window.clearTimeout(hidePopupTimer);
        const $author = $(this);
        const gs = $author.data('gs');
        const hp = $author.data('hp');
        const dblp = $author.data('dblp');
        const or = $author.data('or');
        const name = cleanText($author.text());
        if (!gs && !hp && !dblp && !or) return;

        const links = [
          gs ? `<a href="${gs}" target="_blank" rel="noopener">Google Scholar</a>` : '',
          hp ? `<a href="${hp}" target="_blank" rel="noopener">Homepage</a>` : '',
          dblp ? `<a href="${dblp}" target="_blank" rel="noopener">DBLP</a>` : '',
          or ? `<a href="${or}" target="_blank" rel="noopener">OpenReview</a>` : '',
        ].join('');

        $('#author-popup')
          .html(`<div style="font-weight:700;font-size:14px;margin-bottom:4px;">${name}</div>${links}`)
          .css({ display: 'block', opacity: 1 });
        movePopup(e);
      })
      .on('mousemove.pcPaperlistAuthorPopup', '.author-link', movePopup)
      .on('mouseleave.pcPaperlistAuthorPopup', '.author-link', function () {
        hidePopupTimer = window.setTimeout(() => $('#author-popup').fadeOut(120), 300);
      })
      .on('mouseenter.pcPaperlistAuthorPopup', '#author-popup', function () {
        window.clearTimeout(hidePopupTimer);
      })
      .on('mouseleave.pcPaperlistAuthorPopup', '#author-popup', function () {
        $('#author-popup').fadeOut(80);
      });
  }
});
