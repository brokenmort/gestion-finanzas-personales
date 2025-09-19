document.addEventListener('DOMContentLoaded', () => {
  const token = sessionStorage.getItem('authToken');
  if (!token) { 
    window.location.href = 'index.html'; 
    return; 
  }

  const API_BASE = window.API_BASE || window.location.origin;

  const nameEl = document.getElementById('displayName');       
  const iconEl = document.getElementById('baseProfileIcon');    
  const imgEl  = document.getElementById('baseProfileImage');   

  // ---- Resolver imagen de perfil ----
  const resolveImageUrl = (raw) => {
    if (!raw) return null;              
    const s = String(raw).trim();       
    if (!s) return null;                
    if (/^https?:\/\//i.test(s)) return s; 
    const path = s.startsWith('/') ? s : `/${s}`;
    return `${API_BASE}${path}`;        
  };

  // ---- Cargar datos del usuario ----
  (async () => {
    try {
      const res = await fetch(`${API_BASE}/api/auth/me/`, {
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token 
        },
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
    } catch { window.location.href = 'index.html'; }
  })();

  // ---- Formularios y modales ----
  const addBtn = document.getElementById('add-btn');
  const confirmModal = document.getElementById('confirmModal');
  const successModal = document.getElementById('successModal');
  const confirmChangesBtn = document.getElementById('confirmChangesBtn');
  const cancelChangesBtn = document.getElementById('cancelChangesBtn');
  const successOkBtn = document.getElementById('successOkBtn');

  // Abrir modal de confirmación
  addBtn.onclick = function (e) {
    e.preventDefault();
    confirmModal.style.display = 'flex';
  };

  // Confirmar y guardar en API
  confirmChangesBtn.onclick = async function () {
    const incomeType = document.getElementById('incomeType').value;
    const description = document.getElementById('description').value;
    const amount = document.getElementById('amount').value;
    const date = document.getElementById('date').value;
    const period = document.getElementById('period').value;

    const payload = {
      name: incomeType,
      reason: description,
      quantity: amount,
      period: period, // 🔹 valor seleccionado en el <select>
      date: date
    };

    try {
      const response = await fetch("https://gestion-finanzas-personales-130889bf9a02.herokuapp.com/api/IngresosFijos/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error("Error al guardar el ingreso");
      }

      confirmModal.style.display = 'none';
      successModal.style.display = 'flex';
    } catch (err) {
      confirmModal.style.display = 'none';
      alert("Error: " + err.message);
    }
  };

  // Cerrar modal de confirmación
  cancelChangesBtn.onclick = function () {
    confirmModal.style.display = 'none';
  };

  // Redirigir después de éxito
  successOkBtn.onclick = function () {
    window.location.href = "income.html";
  };
});
