document.addEventListener('DOMContentLoaded', () => {
  const token = sessionStorage.getItem('authToken');
  if (!token) { window.location.href = 'index.html'; return; }

  const API_BASE = window.API_BASE || window.location.origin;
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");

  const addBtn = document.getElementById('add-btn');
  const deleteBtn = document.getElementById('delete-btn');
  const confirmModal = document.getElementById('confirmModal');
  const successModal = document.getElementById('successModal');
  const confirmChangesBtn = document.getElementById('confirmChangesBtn');
  const cancelChangesBtn = document.getElementById('cancelChangesBtn');
  const successOkBtn = document.getElementById('successOkBtn');
  const confirmText = document.getElementById('confirmText');
  const successText = document.getElementById('successText');

  // Si estamos editando
  if (id) {
    addBtn.value = "Save Changes";
    confirmText.textContent = "Do you want to update this expense?";
    successText.textContent = "The expense was updated successfully!";
    deleteBtn.style.display = "inline-block";

    (async () => {
      const res = await fetch(`${API_BASE}/api/EgresosFijos/${id}/`, { headers: { 'Authorization': 'Bearer ' + token }});
      if (res.ok) {
        const data = await res.json();
        document.getElementById("expenseType").value = data.name || "";
        document.getElementById("amount").value = data.quantity || "";
        document.getElementById("periodicity").value = data.period || "monthly";
      }
    })();

    deleteBtn.onclick = async () => {
      if (confirm("Delete this fixed expense?")) {
        await fetch(`${API_BASE}/api/EgresosFijos/${id}/`, {
          method: "DELETE",
          headers: { 'Authorization': 'Bearer ' + token }
        });
        window.location.href = "expenses.html";
      }
    };
  }

  addBtn.onclick = (e) => { e.preventDefault(); confirmModal.style.display = 'flex'; };
  cancelChangesBtn.onclick = () => confirmModal.style.display = 'none';
  successOkBtn.onclick = () => window.location.href = "expenses.html";

  confirmChangesBtn.onclick = async () => {
    const payload = {
      name: document.getElementById("expenseType").value,
      quantity: String(document.getElementById("amount").value),
      period: document.getElementById("periodicity").value
    };

    const url = id ? `${API_BASE}/api/EgresosFijos/${id}/` : `${API_BASE}/api/EgresosFijos/`;
    const method = id ? "PUT" : "POST";

    try {
      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }

      confirmModal.style.display = 'none';
      successModal.style.display = 'flex';
    } catch (err) {
      confirmModal.style.display = 'none';
      alert("Error: " + err.message);
    }
  };
});
