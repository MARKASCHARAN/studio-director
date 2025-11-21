export function hexToRgb(hex){
  const m = hex.replace('#','');
  const bigint = parseInt(m,16);
  return [(bigint>>16)&255, (bigint>>8)&255, bigint&255];
}
