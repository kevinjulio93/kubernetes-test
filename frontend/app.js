let API_BASE = 'http://k8s-api.kevin-space.svc';

async function loadConfig() {
  try {
    const res = await fetch('/config');
    if (!res.ok) return;
    const j = await res.json();
    if (j.API_BASE) API_BASE = j.API_BASE;
  } catch (e) {
    // fallback to default
  }
}

async function fetchMascotas() {
  const res = await fetch(`${API_BASE}/mascotas`);
  if (!res.ok) throw new Error('Error al obtener mascotas');
  const data = await res.json();
  return data.mascotas || [];
}

function renderMascotas(list) {
  const ul = document.getElementById('lista-mascotas');
  ul.innerHTML = '';
  list.forEach(m => {
    const li = document.createElement('li');
    li.className = 'mascota';
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.innerText = `${m.nombre} — ${m.grupo} — ${m.patas} patas — ${m.alimentacion}`;
    const btn = document.createElement('button');
    btn.innerText = 'Eliminar';
    btn.onclick = async () => {
      try {
        const r = await fetch(`${API_BASE}/mascotas/${encodeURIComponent(m.nombre)}`, { method: 'DELETE' });
        if (!r.ok) {
          const err = await r.json();
          alert('Error: ' + (err.error || r.statusText));
          return;
        }
        await loadAndRender();
      } catch (e) {
        alert('Error al eliminar');
      }
    };
    li.appendChild(meta);
    li.appendChild(btn);
    ul.appendChild(li);
  });
}

async function loadAndRender() {
  try {
    const list = await fetchMascotas();
    renderMascotas(list);
  } catch (e) {
    document.getElementById('lista-mascotas').innerText = 'No se pudo cargar la lista: ' + e.message;
  }
}

document.getElementById('form-mascota').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const nombre = document.getElementById('nombre').value.trim();
  const grupo = document.getElementById('grupo').value.trim();
  const patas = parseInt(document.getElementById('patas').value, 10);
  const alimentacion = document.getElementById('alimentacion').value.trim();
  if (!nombre || !grupo || isNaN(patas) || !alimentacion) return alert('Rellena todos los campos');
  try {
    const res = await fetch(`${API_BASE}/mascotas`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, grupo, patas, alimentacion })
    });
    if (res.status === 201) {
      document.getElementById('form-mascota').reset();
      await loadAndRender();
    } else {
      const err = await res.json();
      alert('Error: ' + (err.error || res.statusText));
    }
  } catch (e) {
    alert('Error al agregar mascota');
  }
});

// Inicializar: cargar config y luego la lista
loadConfig().then(() => loadAndRender());
