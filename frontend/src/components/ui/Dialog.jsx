import React from 'react';

export default function Dialog({open, onClose, children}){
  if(!open) return null;
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/40">
      <div className="bg-white p-4 rounded">
        {children}
        <div className="mt-2 text-right"><button onClick={onClose} className="px-2 py-1">Close</button></div>
      </div>
    </div>
  );
}
