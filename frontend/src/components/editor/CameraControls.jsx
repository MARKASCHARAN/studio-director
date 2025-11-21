import React from 'react';

export default function CameraControls(){
  return (
    <div>
      <label>Camera</label>
      <div className="flex gap-2">
        <input className="border p-1" placeholder="position" />
        <input className="border p-1" placeholder="rotation" />
      </div>
    </div>
  );
}
