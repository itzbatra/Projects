import React, {useState} from 'react'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Admin from './pages/Admin'

export default function App(){
  const [token, setToken] = useState(localStorage.getItem('access_token'))
  const [isAdmin, setIsAdmin] = useState(localStorage.getItem('is_admin') === '1')
  if(!token) return <Login onLogin={(t, isAdminFlag)=>{localStorage.setItem('access_token', t); setToken(t); localStorage.setItem('is_admin', isAdminFlag? '1':'0'); setIsAdmin(isAdminFlag)}} />
  return isAdmin ? <Admin token={token} onLogout={()=>{localStorage.removeItem('access_token'); setToken(null)}}/> : <Dashboard token={token} onLogout={()=>{localStorage.removeItem('access_token'); setToken(null)}}/>
}
