export async function postJSON(endpoint, payload){
  const res = await fetch(endpoint, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
  return res.json();
}
