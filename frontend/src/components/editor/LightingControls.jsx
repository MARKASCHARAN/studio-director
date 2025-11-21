import React from 'react';

export default function LightingControls(){
  return (
    <div>
      <label>Lighting</label>
      <input type="range" min="0" max="100" />
    </div>
  );
}
