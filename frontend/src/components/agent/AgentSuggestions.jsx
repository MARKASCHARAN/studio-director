import React from 'react';

export default function AgentSuggestions({suggestions=[]}){
  return (
    <div>
      <h4 className="font-semibold">Suggestions</h4>
      <ul>
        {suggestions.map((s,i)=> <li key={i}>{s}</li>)}
      </ul>
    </div>
  );
}
