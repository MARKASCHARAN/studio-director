import React, {useState} from 'react';

export default function Tabs({tabs}){
  const [i, setI] = useState(0);
  return (
    <div>
      <div className="flex space-x-2">
        {tabs.map((t, idx)=> (
          <button key={t.title} onClick={()=>setI(idx)} className={`px-2 py-1 ${idx===i? 'bg-gray-200':''}`}>{t.title}</button>
        ))}
      </div>
      <div className="mt-2">{tabs[i].content}</div>
    </div>
  );
}
