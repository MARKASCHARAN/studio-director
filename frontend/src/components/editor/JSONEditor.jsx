import React from 'react';

export default function JSONEditor({value, onChange}){
  return (
    <textarea className="w-full h-64 p-2 font-mono" value={JSON.stringify(value, null, 2)} onChange={(e)=>{
      try{ onChange(JSON.parse(e.target.value)); }catch(err){/* ignore parse errors */}
    }} />
  );
}
