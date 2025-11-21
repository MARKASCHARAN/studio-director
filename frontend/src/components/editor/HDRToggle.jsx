import React from 'react';

export default function HDRToggle({on, onToggle}){
  return (
    <label className="flex items-center gap-2">
      <input type="checkbox" checked={on} onChange={e=>onToggle(e.target.checked)} /> HDR
    </label>
  );
}
