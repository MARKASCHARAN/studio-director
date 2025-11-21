import React from 'react';

export default function Panel({children, title}){
  return (
    <section className="p-4 bg-white rounded shadow-sm">
      {title && <h3 className="font-medium mb-2">{title}</h3>}
      {children}
    </section>
  );
}
