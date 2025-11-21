export function validateJSON(obj){
  try{ JSON.stringify(obj); return true; }catch(e){return false;}
}
