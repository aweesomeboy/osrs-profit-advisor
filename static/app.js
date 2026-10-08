let currentPage = 1;
let currentSort = 'name';
let currentOrder = 'asc';
let currentSearch = '';
let pageSize = 20;

const statusEl = document.getElementById('apiStatus');
const lastSyncEl = document.getElementById('lastSync');
const apiStatusCard = document.getElementById('apiStatusCard');
const lastSyncCard = document.getElementById('lastSyncCard');
const nextSyncCard = document.getElementById('nextSyncCard');
const itemsLoadedCard = document.getElementById('itemsLoadedCard');
const staleWarning = document.getElementById('staleWarning');
const errorAlert = document.getElementById('errorAlert');
const tableBody = document.getElementById('tableBody');
const loadingState = document.getElementById('loadingState');

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function updateHealth(health) {
  const ok = health.status === 'ok';
  statusEl.textContent = ok ? 'API: live' : 'API: error';
  statusEl.style.color = ok ? '#5fe08a' : '#ff9a9a';
  apiStatusCard.textContent = ok ? 'Connected' : 'Error';
  apiStatusCard.style.color = ok ? '#5fe08a' : '#ff9a9a';

  const syncText = health.last_sync ? new Date(health.last_sync).toLocaleString() : 'Never';
  lastSyncEl.textContent = `Last sync: ${syncText}`;
  lastSyncCard.textContent = syncText;

  if (health.next_sync) {
    nextSyncCard.textContent = new Date(health.next_sync).toLocaleString();
  } else {
    nextSyncCard.textContent = '—';
  }

  itemsLoadedCard.textContent = String(health.item_count || 0);
  staleWarning.classList.toggle('hidden', !health.stale);

  if (health.error) {
    errorAlert.textContent = health.error;
    errorAlert.classList.remove('hidden');
  } else {
    errorAlert.classList.add('hidden');
  }
}

async function loadHealth() {
  try {
    const health = await fetchJson('/api/health');
    updateHealth(health);
  } catch (error) {
    statusEl.textContent = 'API: unavailable';
    statusEl.style.color = '#ff9a9a';
    apiStatusCard.textContent = 'Unavailable';
    apiStatusCard.style.color = '#ff9a9a';
    errorAlert.textContent = 'Unable to connect to the local backend.';
    errorAlert.classList.remove('hidden');
  }
}

async function loadItems() {
  loadingState.style.display = 'block';
  try {
    const params = new URLSearchParams({
      search: currentSearch,
      sort: currentSort,
      order: currentOrder,
      page: String(currentPage),
      page_size: String(pageSize),
    });
    const payload = await fetchJson(`/api/items?${params.toString()}`);
    renderTable(payload.items || []);
    renderPagination(payload);
    loadingState.style.display = 'none';
  } catch (error) {
    tableBody.innerHTML = '<tr><td colspan="8">Unable to load item data.</td></tr>';
    errorAlert.textContent = error.message || 'Failed to load item data.';
    errorAlert.classList.remove('hidden');
    loadingState.style.display = 'none';
  }
}

function renderTable(items) {
  if (!items.length) {
    tableBody.innerHTML = '<tr><td colspan="8">No items match the current filter.</td></tr>';
    return;
  }

  tableBody.innerHTML = items.map((item) => {
    const margin = item.margin == null ? 'N/A' : formatNumber(item.margin);
    const marginClass = item.margin == null ? 'neutral' : (item.margin >= 0 ? 'positive' : 'negative');
    const roi = item.roi == null ? 'N/A' : `${Number(item.roi).toFixed(2)}%`;
    const roiClass = item.roi == null ? 'neutral' : (item.roi >= 0 ? 'positive' : 'negative');
    const buyPrice = item.high_price == null ? 'N/A' : formatNumber(item.high_price);
    const sellPrice = item.low_price == null ? 'N/A' : formatNumber(item.low_price);
    const buyLimit = item.buy_limit == null ? '—' : formatNumber(item.buy_limit);
    const updateLabel = item.last_update ? new Date(item.last_update).toLocaleString() : 'N/A';

    return `
      <tr>
        <td>${escapeHtml(item.name || 'Unknown')}</td>
        <td>${item.item_id}</td>
        <td>${buyPrice}</td>
        <td>${sellPrice}</td>
        <td class="${marginClass}">${margin}</td>
        <td class="${roiClass}">${roi}</td>
        <td>${buyLimit}</td>
        <td>${updateLabel}</td>
      </tr>
    `;
  }).join('');
}

function formatNumber(value) {
  if (value == null || Number.isNaN(Number(value))) return 'N/A';
  return Number(value).toLocaleString();
}

function renderPagination(payload) {
  const pagination = document.getElementById('pagination');
  const totalPages = payload.total_pages || 1;
  const page = payload.page || 1;

  const buttons = [];
  for (let i = 1; i <= totalPages; i++) {
    buttons.push(`<button class="${i === page ? 'active' : ''}" data-page="${i}">${i}</button>`);
  }

  pagination.innerHTML = buttons.join('');
  pagination.querySelectorAll('button').forEach((button) => {
    button.addEventListener('click', () => {
      currentPage = Number(button.dataset.page);
      loadItems();
    });
  });
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

document.getElementById('searchInput').addEventListener('input', (event) => {
  currentSearch = event.target.value.trim();
  currentPage = 1;
  loadItems();
});

document.getElementById('sortBy').addEventListener('change', (event) => {
  currentSort = event.target.value;
  currentPage = 1;
  loadItems();
});

document.getElementById('sortOrder').addEventListener('change', (event) => {
  currentOrder = event.target.value;
  currentPage = 1;
  loadItems();
});

document.getElementById('pageSize').addEventListener('change', (event) => {
  pageSize = Number(event.target.value);
  currentPage = 1;
  loadItems();
});

document.getElementById('refreshBtn').addEventListener('click', async () => {
  try {
    await fetchJson('/api/refresh', { method: 'POST' });
    await loadHealth();
    await loadItems();
  } catch (error) {
    errorAlert.textContent = 'Refresh request failed.';
    errorAlert.classList.remove('hidden');
  }
});

loadHealth();
loadItems();
setInterval(() => {
  loadHealth();
  loadItems();
}, 60000);
