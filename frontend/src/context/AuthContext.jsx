import { createContext, useContext, useMemo, useState } from 'react'
import api from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('careerpilot_token'))
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem('careerpilot_user')
    return raw ? JSON.parse(raw) : null
  })

  const login = async (values) => {
    const { data } = await api.post('/auth/login', values)
    const authToken = data.data.access_token
    localStorage.setItem('careerpilot_token', authToken)
    localStorage.setItem('careerpilot_user', JSON.stringify(data.data.user))
    setToken(authToken)
    setUser(data.data.user)
  }

  const signup = async (values) => {
    await api.post('/auth/signup', values)
    await login({ email: values.email, password: values.password })
  }

  const logout = () => {
    localStorage.removeItem('careerpilot_token')
    localStorage.removeItem('careerpilot_user')
    setToken(null)
    setUser(null)
  }

  const value = useMemo(() => ({ token, user, login, signup, logout, isAuthenticated: Boolean(token) }), [token, user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
