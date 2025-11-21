import React from 'react';

export default function PalettePicker({palettes = [], onPick=()=>{}}){
  return (
    <div className="flex gap-2">
      {palettes.map((p, idx)=> (
        <button key={idx} className="w-8 h-8" style={{background: p[0]}} onClick={()=>onPick(p)} />
      ))}
    </div>
  );
}
