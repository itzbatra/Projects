import React, {useEffect, useState} from 'react'
import axios from 'axios'
export default function Admin({token, onLogout}){
  const [users,setUsers]=useState([])
  useEffect(()=>{ axios.get((import.meta.env.VITE_API_URL||'http://localhost:5000') + '/admin/users', {headers:{Authorization:'Bearer '+token}}).then(r=>setUsers(r.data)).catch(e=>console.error(e)) },[])
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Admin Panel</h2>
        <button className="px-3 py-1 bg-red-500 text-white rounded" onClick={onLogout}>Logout</button>
      </div>
      <h3 className="font-semibold">Users</h3>
      <ul className="mt-2 space-y-2">{users.map(u=> <li key={u.id} className="bg-white p-2 rounded shadow">{u.email} — {u.role}</li>)}</ul>
    </div>
  )
}
