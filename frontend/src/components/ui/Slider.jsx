import React from 'react';

export default function Slider({value, onChange, min=0, max=100}){
  return (
    <input type="range" min={min} max={max} value={value} onChange={e=>onChange(Number(e.target.value))} />
  );
}
