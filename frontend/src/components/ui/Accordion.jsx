import React, {useState} from 'react';

export default function Accordion({title, children}){
  const [open, setOpen] = useState(false);
  return (
    <div className="border rounded">
      <button className="w-full text-left p-2" onClick={()=>setOpen(!open)}>{title}</button>
      {open && <div className="p-2">{children}</div>}
    </div>
  );
}
