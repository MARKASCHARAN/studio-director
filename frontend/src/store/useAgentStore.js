import create from 'zustand';

export const useAgentStore = create(set => ({
  suggestions: [],
  setSuggestions: (s) => set({suggestions: s}),
}));
