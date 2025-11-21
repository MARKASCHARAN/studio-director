import create from 'zustand';

export const useProjectStore = create(set => ({
  project: null,
  setProject: (p) => set({project: p}),
}));
