const BASE = 'http://localhost:5000/api';

function headers() {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  return {
    'Content-Type': 'application/json',
    'Authorization': user.id ? `Bearer ${user.id}` : ''
  };
}

export async function getFavorites() {
  const res = await fetch(`${BASE}/favorites`, { headers: headers() });
  return res.json();
}

export async function addFavorite(item) {
  const res = await fetch(`${BASE}/favorites`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify(item)
  });
  return res.json();
}

export async function delFavorite(item) {
  const res = await fetch(`${BASE}/favorites`, {
    method: 'DELETE',
    headers: headers(),
    body: JSON.stringify({ type: item.type, key: item.key })
  });
  return res.json();
}