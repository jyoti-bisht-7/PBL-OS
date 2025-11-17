// filepath: intrusion-resistant-pms-phase3/gui/static/js/chart.js
document.addEventListener('DOMContentLoaded', function() {
  if (typeof lucide !== 'undefined' && lucide.createIcons) {
    lucide.createIcons();
  } else {
    console.warn('Lucide not loaded, skipping icon creation.');
  }
  // Only call initialize(), which itself calls initializeCharts()
  initialize();
});

let cpuChart = null;
let memoryChart = null;
let currentFilter = 'all';
let allProcesses = [];

const API_BASE = '/api';
const UPDATE_INTERVAL = 5000; // 5 seconds

async function fetchActiveProcesses() {
  try {
    const response = await fetch(`${API_BASE}/active-processes`);
    if (!response.ok) throw new Error('Failed to fetch active processes');
    allProcesses = await response.json();
    return allProcesses;
  } catch (error) {
    console.error('Error fetching active processes:', error);
  }
}

async function fetchCPUMemoryUsage() {
  try {
    const response = await fetch(`${API_BASE}/cpu-memory-usage`);
    if (!response.ok) throw new Error('Failed to fetch CPU and memory usage');
    return await response.json();
  } catch (error) {
    console.error('Error fetching CPU and memory usage:', error);
  }
}

async function fetchIntrusionAlerts() {
  try {
    const response = await fetch(`${API_BASE}/intrusion-alerts`);
    if (!response.ok) throw new Error('Failed to fetch intrusion alerts');
    return await response.json();
  } catch (error) {
    console.error('Error fetching intrusion alerts:', error);
  }
}

async function fetchHistoricalData() {
  try {
    const response = await fetch(`${API_BASE}/historical-data`);
    if (!response.ok) throw new Error('Failed to fetch historical data');
    return await response.json();
  } catch (error) {
    console.error('Error fetching historical data:', error);
    return { cpu: [], memory: [] };
  }
}

function determineStatus(proc) {
  const cpu = proc.cpu || 0;
  const memory = proc.memory || 0;
  
  if (cpu > 70 || memory > 80) {
    return 'suspicious';
  } else {
    return 'safe';
  }
}

async function updateMetrics() {
  const usage = await fetchCPUMemoryUsage();
  const processes = await fetchActiveProcesses();
  const alerts = await fetchIntrusionAlerts();

  document.getElementById('cpuMetric').textContent = `${usage.cpu}%`;
  document.getElementById('memMetric').textContent = `${usage.memory}%`;
  document.getElementById('processCount').textContent = processes.length;

  const criticalAlerts = alerts.filter(a => a.type === 'CPU_HOG' || a.type === 'FORK_BOMB_SUSPECT');
  document.getElementById('alertCount').textContent = `${alerts.length} Alert${alerts.length !== 1 ? 's' : ''}`;
  document.getElementById('threatsBlocked').textContent = criticalAlerts.length;

  updateTrends(usage);
}

function updateTrends(usage) {
  const cpuTrend = usage.cpu > 50 ? '↑ High' : '↓ Normal';
  const memTrend = usage.memory > 60 ? '↑ High' : '↓ Normal';
  
  document.getElementById('cpuTrend').textContent = cpuTrend;
  document.getElementById('memTrend').textContent = memTrend;
}

function initializeCharts() {
  const cpuCanvas = document.getElementById('cpuChart');
  const memCanvas = document.getElementById('memoryChart');
  if (!cpuCanvas || !memCanvas) {
    console.error('Chart canvas elements not found:', { cpuCanvas, memCanvas });
    return;
  }
  const cpuCtx = cpuCanvas.getContext('2d');
  cpuChart = new Chart(cpuCtx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'CPU Usage (%)',
        data: [],
        borderColor: '#00ffcc',
        backgroundColor: 'rgba(0, 255, 204, 0.1)',
        fill: true,
        tension: 0.4,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { 
          beginAtZero: true, 
          max: 100,
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#8b95a5' }
        },
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#8b95a5' }
        }
      }
    }
  });

  const memCtx = memCanvas.getContext('2d');
  memoryChart = new Chart(memCtx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Memory Usage (%)',
        data: [],
        borderColor: '#ffaa00',
        backgroundColor: 'rgba(255,170,0,0.1)',
        fill: true,
        tension: 0.4,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { 
          beginAtZero: true, 
          max: 100,
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#8b95a5' }
        },
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#8b95a5' }
        }
      }
    }
  });
  console.log('Charts initialized:', { cpuChart, memoryChart });
}

// Add this function to update the charts with real data
async function updateCharts() {
  const hist = await fetchHistoricalData();
  console.log('Fetched historical data:', hist);
  const cpuLabels = hist.cpu.map(d => d.time);
  const cpuData = hist.cpu.map(d => d.value);
  const memLabels = hist.memory.map(d => d.time);
  const memData = hist.memory.map(d => d.value);
  console.log('CPU labels:', cpuLabels);
  console.log('CPU data:', cpuData);
  console.log('Memory labels:', memLabels);
  console.log('Memory data:', memData);

  if (cpuChart && memoryChart) {
    console.log('Updating charts...');
    cpuChart.data.labels = cpuLabels;
    cpuChart.data.datasets[0].data = cpuData;
    cpuChart.update();

    memoryChart.data.labels = memLabels;
    memoryChart.data.datasets[0].data = memData;
    memoryChart.update();
    console.log('Charts updated.');
  } else {
    console.warn('Chart objects not initialized:', { cpuChart, memoryChart });
  }
}

async function loadProcessTable(filter = 'all', search = '') {
  const tableBody = document.getElementById('processTable');
  if (allProcesses.length === 0) {
    await fetchActiveProcesses();
  }
  const filtered = allProcesses.filter(proc => {
    const matchesFilter = filter === 'all' || determineStatus(proc) === filter;
    const matchesSearch = proc.name && proc.name.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });
  if (filtered.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 30px;">No processes found.</td></tr>';
    return;
  }
  tableBody.innerHTML = '';
  filtered.forEach(proc => {
    const status = determineStatus(proc);
    let statusClass = 'safe';
    if (status === 'suspicious') statusClass = 'suspicious';
    if (proc.cpu > 90 || proc.memory > 90) statusClass = 'critical';
    // Highlight python.exe with high CPU
    let highlightRow = '';
    if (proc.name && proc.name.toLowerCase().includes('python') && proc.cpu > 70) {
      highlightRow = ' style="background:#ffefef"';
    }
    const row = document.createElement('tr');
    row.setAttribute('style', highlightRow);
    row.innerHTML = `
      <td>${proc.pid}</td>
      <td>${proc.name}</td>
      <td>${proc.user}</td>
      <td>${proc.cpu}%</td>
      <td>${proc.memory}%</td>
      <td>
        <span class="status-badge ${statusClass}">${statusClass.charAt(0).toUpperCase() + statusClass.slice(1)}</span>
      </td>
      <td>${proc.state}</td>
      <td>
        <button class="action-btn throttle" onclick="throttleProcess(${proc.pid})">Throttle</button>
        <button class="action-btn terminate" onclick="terminateProcess(${proc.pid})">Terminate</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

async function loadAlerts() {
  const alertsContainer = document.getElementById('alertsContainer');
  const alerts = await fetchIntrusionAlerts();
  if (!alerts || alerts.length === 0) {
    alertsContainer.innerHTML = '<div class="alert-card info"><div class="alert-title">No active alerts.</div></div>';
    return;
  }
  alertsContainer.innerHTML = '';
  alerts.forEach(alert => {
    const alertType = determineAlertType(alert.type);
    const alertCard = document.createElement('div');
    alertCard.className = `alert-card ${alertType.class}`;
    let message = formatAlertMessage(alert);
    if (alert.type === 'CPU_HOG' && alert.name && alert.cpu) {
      message += ` [${alert.name} (PID ${alert.pid}) CPU: ${alert.cpu}%]`;
    }
    alertCard.innerHTML = `
      <i data-lucide="${alertType.icon}" class="alert-icon" style="color: ${alertType.color};"></i>
      <div class="alert-content">
        <div class="alert-title">${formatAlertTitle(alert.type)}</div>
        <div class="alert-message">${message}</div>
      </div>
    `;
    alertsContainer.appendChild(alertCard);
  });
  if (typeof lucide !== 'undefined' && lucide.createIcons) {
    lucide.createIcons();
  } else {
    console.warn('Lucide not loaded, skipping icon creation in alerts.');
  }
}

function determineAlertType(type) {
  const types = {
    'CPU_HOG': { class: 'critical', icon: 'alert-octagon', color: '#ff4d4d' },
    'FORK_BOMB_SUSPECT': { class: 'critical', icon: 'alert-triangle', color: '#ff4d4d' },
    'ERROR': { class: 'warning', icon: 'alert-triangle', color: '#ffaa00' },
    'DEFAULT': { class: 'info', icon: 'info', color: '#00bfff' }
  };
  return types[type] || types['DEFAULT'];
}

function formatAlertTitle(type) {
  const titles = {
    'CPU_HOG': 'High CPU Usage Detected',
    'FORK_BOMB_SUSPECT': 'Fork Bomb Suspected',
    'ERROR': 'System Error',
    'DEFAULT': 'Security Alert'
  };
  return titles[type] || titles['DEFAULT'];
}

function formatAlertMessage(alert) {
  if (alert.type === 'CPU_HOG') {
    return `CPU usage exceeded threshold: ${alert.cpu}%`;
  } else {
    return JSON.stringify(alert);
  }
}

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    currentFilter = this.dataset.filter;
    loadProcessTable(currentFilter);
  });
});

document.getElementById('searchBox').addEventListener('input', function() {
  loadProcessTable(currentFilter, this.value);
});

document.querySelectorAll('.chart-btn[data-timerange]').forEach(btn => {
  btn.addEventListener('click', function() {
    // Implement time range logic here
  });
});

async function throttleProcess(pid) {
  try {
    const response = await fetch(`${API_BASE}/throttle-process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pid: Number(pid) })
    });
    const result = await response.json();
    if (response.ok && result.success) {
      alert(`Process ${pid} throttled successfully.`);
      loadProcessTable(currentFilter);
    } else {
      alert(`Failed to throttle process: ${result.error || 'Unknown error.'}`);
    }
  } catch (error) {
    alert('Error throttling process: ' + error);
    console.error('Error throttling process:', error);
  }
}

async function terminateProcess(pid) {
  try {
    const response = await fetch(`${API_BASE}/terminate-process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pid: Number(pid) })
    });
    const result = await response.json();
    if (response.ok && result.success) {
      alert(`Process ${pid} terminated successfully.`);
      loadProcessTable(currentFilter);
    } else {
      alert(`Failed to terminate process: ${result.error || 'Unknown error.'}`);
    }
  } catch (error) {
    alert('Error terminating process: ' + error);
    console.error('Error terminating process:', error);
  }
}

async function refreshData() {
  await updateMetrics();
  await loadProcessTable(currentFilter);
  await loadAlerts();
  await updateCharts(); // <-- add this line
}

function startAutoRefresh() {
  setInterval(refreshData, UPDATE_INTERVAL);
}

async function initialize() {
  initializeCharts();
  await refreshData();
  startAutoRefresh();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initialize);
} else {
  initialize();
}
