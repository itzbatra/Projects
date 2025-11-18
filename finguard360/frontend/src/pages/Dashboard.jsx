import React, {useEffect, useState, useRef} from 'react'
import axios from 'axios'
import { Chart } from 'chart.js/auto'
export default function Dashboard({token, onLogout}){
  const [txns, setTxns] = useState([])
  const canvasRef = useRef()
  useEffect(()=>{
    axios.get((import.meta.env.VITE_API_URL || 'http://localhost:5000') + '/transactions', {headers: {Authorization: 'Bearer ' + token}})
      .then(r=> { setTxns(r.data); renderChart(r.data) })
      .catch(e=> { console.error(e); if(e.response && e.response.status===401) onLogout() })
  },[])
  function renderChart(data){
    const ctx = canvasRef.current.getContext('2d')
    const amounts = data.slice(0,10).map(d=>d.amount)
    const labels = data.slice(0,10).map((d,i)=>d.txn_date)
    new Chart(ctx, {type:'bar', data:{labels, datasets:[{label:'Recent spending', data:amounts}]}})
  }
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Dashboard</h2>
        <button className="px-3 py-1 bg-red-500 text-white rounded" onClick={onLogout}>Logout</button>
      </div>
      <canvas ref={canvasRef} width="800" height="250"></canvas>
      <h3 className="mt-4 font-semibold">Recent transactions</h3>
      <ul className="mt-2 space-y-2">{txns.map(t=> <li key={t.id} className="bg-white p-2 rounded shadow">{t.txn_date}: ${t.amount} — {t.category} — {t.description}</li>)}</ul>
    </div>
  )
}
