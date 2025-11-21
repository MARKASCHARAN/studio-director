import create from 'zustand';

export const useJSONStore = create(set => ({
  data: {},
  setData: (d) => set({data: d}),
}));
