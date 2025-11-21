import {useState} from 'react';

export default function useGenerate(){
  const [loading, setLoading] = useState(false);
  const generate = async (json) => { setLoading(true); try{ /* call API */ }finally{setLoading(false);} };
  return {generate, loading};
}
