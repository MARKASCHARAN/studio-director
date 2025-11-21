import React from 'react';

export default function Sidebar() {
  return (
    <aside className="w-64 p-4 bg-gray-50 border-r">
      <h2 className="font-bold mb-4">Sidebar</h2>
      <nav>
        <ul>
          <li>Dashboard</li>
          <li>Editor</li>
          <li>Outputs</li>
        </ul>
      </nav>
    </aside>
  );
}
