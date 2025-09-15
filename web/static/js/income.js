// Esperamos a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', async () => {
    
    // Recuperamos el token de autenticación guardado en sessionStorage
    const token = sessionStorage.getItem('authToken');

    if (!token) { 
        window.location.href = 'index.html'; 
        return; 
    }

    const API_BASE = window.API_BASE || window.location.origin;

    const nameEl = document.getElementById('incomeUsername');       
    const iconEl = document.getElementById('walletProfileIcon');    
    const imgEl  = document.getElementById('walletProfileImage');   

    const resolveImageUrl = (raw) => {
        if (!raw) return null;              
        const s = String(raw).trim();       
        if (!s) return null;                
        if (/^https?:\/\//i.test(s)) return s; 
        const path = s.startsWith('/') ? s : `/${s}`;
        return `${API_BASE}${path}`;        
    };

    try {
        const res = await fetch(`${API_BASE}/api/auth/me/`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
        });

        if (!res.ok) throw new Error('No autorizado');
        const data = await res.json();

        if (nameEl) {
            nameEl.textContent = data.first_name || data.email || 'Usuario';
        }

        const url = resolveImageUrl(data && data.profile_image);

        if (url && imgEl && iconEl) {
            imgEl.onload = () => { 
                imgEl.style.display = 'block'; 
                iconEl.style.display = 'none'; 
            };
            imgEl.onerror = () => { 
                imgEl.style.display = 'none'; 
                iconEl.style.display = 'block'; 
            };
            imgEl.src = url + (url.includes('?') ? `&t=${Date.now()}` : `?t=${Date.now()}`);
        }
    } catch (e) {
        window.location.href = 'index.html';
    }

    // --- Cargar ingresos dinámicamente ---
    async function loadIngresos() {
      try {
        // Ingresos Fijos
        const resFijos = await fetch(`${API_BASE}/api/IngresosFijos/`, {
          headers: { 'Authorization': 'Bearer ' + token }
        });
        if (resFijos.ok) {
          const dataFijos = await resFijos.json();
          const tbodyFijos = document.querySelector('.fixed-table tbody');
          tbodyFijos.innerHTML = '';

          dataFijos.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${item.name}</td>
              <td>${item.reason}</td>
              <td>${item.quantity}</td>
              <td>${item.period || ''}</td>
            `;
            tbodyFijos.appendChild(tr);
          });
        }

        // Ingresos Extra
        const resExtra = await fetch(`${API_BASE}/api/IngresosExtra/`, {
          headers: { 'Authorization': 'Bearer ' + token }
        });
        if (resExtra.ok) {
          const dataExtra = await resExtra.json();
          const tbodyExtra = document.querySelector('.supp-table tbody');
          tbodyExtra.innerHTML = '';

          dataExtra.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>${item.name}</td>
              <td>${item.quantity}</td>
              <td>${item.date}</td>
            `;
            tbodyExtra.appendChild(tr);
          });
        }
      } catch (err) {
        console.error('Error cargando ingresos:', err);
      }
    }

    loadIngresos();
});
