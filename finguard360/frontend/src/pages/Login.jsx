import React, {useState} from 'react'
import axios from 'axios'
export default function Login({onLogin}){
  const [email,setEmail]=useState('admin@example.com')
  const [pw,setPw]=useState('password')
  const [err,setErr]=useState('')
  async function submit(e){
    e.preventDefault()
    try{
      const r = await axios.post((import.meta.env.VITE_API_URL || 'http://localhost:5000') + '/auth/login', {email, password: pw})
      const isAdmin = false
      onLogin(r.data.access_token, isAdmin)
    }catch(e){
      setErr('login failed')
    }
  }
  return (
    <div className="max-w-md mx-auto p-6 bg-white mt-20 rounded shadow">
      <h2 className="text-2xl font-bold mb-4">FinGuard 360 — Login</h2>
      <form onSubmit={submit} className="space-y-3">
        <input className="w-full p-2 border rounded" value={email} onChange={e=>setEmail(e.target.value)} />
        <input type="password" className="w-full p-2 border rounded" value={pw} onChange={e=>setPw(e.target.value)} />
        <button className="px-4 py-2 bg-blue-600 text-white rounded">Login</button>
      </form>
      <div className="text-red-600">{err}</div>
    </div>
  )
}
