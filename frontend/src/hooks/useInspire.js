import {useState} from 'react';

export default function useInspire(){
  const [loading, setLoading] = useState(false);
  const inspire = async (img) => { setLoading(true); try{}finally{setLoading(false);} };
  return {inspire, loading};
}
