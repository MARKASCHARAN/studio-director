import {useState} from 'react';

export default function useRefine(){
  const [loading, setLoading] = useState(false);
  const refine = async (patch) => { setLoading(true); try{}finally{setLoading(false);} };
  return {refine, loading};
}
