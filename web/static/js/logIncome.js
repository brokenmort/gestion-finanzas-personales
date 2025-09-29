document.addEventListener('DOMContentLoaded', async () => {
  const token = sessionStorage.getItem('authToken');
  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  const API_BASE = window.API_BASE || window.location.origin;

  const nameEl = document.getElementById('displayName');
  const iconEl = document.getElementById('baseProfileIcon');
  const imgEl = document.getElementById('baseProfileImage');

  const resolveImageUrl = (raw) => {
    if (!raw) return null;
    const s = String(raw).trim();
    if (!s) return null;
    if (/^https?:\/\//i.test(s)) return s;
    const path = s.startsWith('/') ? s : `/${s}`;
    return `${API_BASE}${path}`;
  };

  // --- Cargar usuario ---
  try {
    const res = await fetch(`${API_BASE}/api/auth/me/`, {
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
    });
    if (!res.ok) throw new Error('No autorizado');
    const data = await res.json();
    if (nameEl) nameEl.textContent = data.first_name || data.email || 'Usuario';
    const url = resolveImageUrl(data && data.profile_image);
    if (url && imgEl && iconEl) {
      imgEl.onload = () => { imgEl.style.display = 'block'; iconEl.style.display = 'none'; };
      imgEl.onerror = () => { imgEl.style.display = 'none'; iconEl.style.display = 'block'; };
      imgEl.src = url + (url.includes('?') ? `&t=${Date.now()}` : `?t=${Date.now()}`);
    }
  } catch {
    window.location.href = 'index.html';
  }

  // --- Cargar ingresos fijos ---
  const incomeSelect = document.getElementById('income');
  let ingresosFijos = [];
  try {
    const res = await fetch(`${API_BASE}/api/IngresosFijos/`, {
      headers: { 'Authorization': 'Bearer ' + token }
    });
    if (res.ok) {
      ingresosFijos = await res.json();
      incomeSelect.innerHTML = '<option value="">-- Select --</option>';
      ingresosFijos.forEach(ing => {
        const opt = document.createElement('option');
        opt.value = ing.id;
        opt.textContent = `${ing.name} (${ing.period})`;
        incomeSelect.appendChild(opt);
      });
    }
  } catch (err) {
    console.error('Error cargando ingresos fijos:', err);
  }

  // --- Manejo de vistas (log vs history) ---
  const logButton = document.querySelector('.log-button');
  const logForm = document.querySelector('.log-form');
  const historyTable = document.querySelector('.history-table');
  const historyBtn = document.getElementById('history');
  const logDetailsBtn = document.getElementById('logDetails');
  const logDetailsSelect = document.getElementById('logDetailsSelect');
  const historyBody = document.getElementById('historyBody');

  historyBtn.onclick = function () {
    historyTable.style.display = 'block';
    logForm.style.display = 'none';
    logButton.style.display = 'none';
    loadHistory();
  };

  logDetailsBtn.onclick = logDetailsSelect.onclick = function () {
    logForm.style.display = 'block';
    historyTable.style.display = 'none';
    logButton.style.display = 'flex';
  };

  // --- Guardar pago ---
  const saveBtn = document.getElementById('save-btn');
  const confirmModal = document.getElementById('confirmModal');
  const successModal = document.getElementById('successModal');
  const confirmChangesBtn = document.getElementById('confirmChangesBtn');
  const cancelChangesBtn = document.getElementById('cancelChangesBtn');
  const successOkBtn = document.getElementById('successOkBtn');

  saveBtn.onclick = function (e) {
    e.preventDefault();
    confirmModal.style.display = 'flex';
  };

  confirmChangesBtn.onclick = async function () {
    const incomeId = incomeSelect.value;
    const amount = document.getElementById('amount').value;
    const date = document.getElementById('date').value;

    if (!incomeId || !amount || !date) {
      alert("Please fill all fields");
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/IngresosFijos/${incomeId}/pagos/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ amount: String(amount), date: date })
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(err);
      }

      confirmModal.style.display = 'none';
      successModal.style.display = 'flex';
    } catch (err) {
      confirmModal.style.display = 'none';
      alert("Error: " + err.message);
    }
  };

  cancelChangesBtn.onclick = () => { confirmModal.style.display = 'none'; };
  successOkBtn.onclick = () => { window.location.href = "./income.html"; };

  // --- Cargar historial de pagos ---
  async function loadHistory() {
    historyBody.innerHTML = '';
    for (let ing of ingresosFijos) {
      try {
        const res = await fetch(`${API_BASE}/api/IngresosFijos/${ing.id}/pagos/`, {
          headers: { 'Authorization': 'Bearer ' + token }
        });
        if (res.ok) {
          const pagos = await res.json();
          pagos.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${ing.name}</td><td>${p.amount}</td><td>${p.date}</td>`;
            historyBody.appendChild(tr);
          });
        }
      } catch (err) {
        console.error('Error cargando historial:', err);
      }
    }
  }
});
