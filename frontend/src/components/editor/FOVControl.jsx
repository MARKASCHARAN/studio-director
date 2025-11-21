import React from 'react';

export default function FOVControl({value=60, onChange=()=>{}}){
  return (
    <div>
      <label>FOV: {value}</label>
      <input type="range" min="1" max="120" value={value} onChange={e=>onChange(Number(e.target.value))} />
    </div>
  );
}
