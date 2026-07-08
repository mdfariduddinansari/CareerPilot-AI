import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const schema = z.object({
  name: z.string().min(2).optional(),
  email: z.string().email(),
  password: z.string().min(6)
})

export default function AuthPage({ mode }) {
  const [error, setError] = useState('')
  const { isAuthenticated, login, signup } = useAuth()
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({ resolver: zodResolver(schema) })

  if (isAuthenticated) return <Navigate to="/" replace />

  const onSubmit = async (values) => {
    try {
      setError('')
      if (mode === 'signup') await signup(values)
      else await login(values)
    } catch (e) {
      setError(e.response?.data?.message || 'Authentication failed')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <form onSubmit={handleSubmit(onSubmit)} className="w-full max-w-md rounded-xl border border-slate-200 bg-white p-6 shadow dark:border-slate-800 dark:bg-slate-900">
        <h1 className="mb-1 text-2xl font-bold">CareerPilot AI</h1>
        <p className="mb-4 text-sm text-slate-500">Everything you need to land your dream job — powered by AI.</p>
        {mode === 'signup' && <input className="mb-2 w-full rounded border p-2 bg-transparent" placeholder="Name" {...register('name')} />}
        <input className="mb-2 w-full rounded border p-2 bg-transparent" placeholder="Email" {...register('email')} />
        <input type="password" className="mb-2 w-full rounded border p-2 bg-transparent" placeholder="Password" {...register('password')} />
        {(errors.email || errors.password) && <p className="mb-2 text-sm text-rose-500">Please enter valid credentials.</p>}
        {error && <p className="mb-2 text-sm text-rose-500">{error}</p>}
        <button disabled={isSubmitting} className="w-full rounded bg-indigo-600 p-2 text-white">{isSubmitting ? 'Please wait...' : mode === 'signup' ? 'Create account' : 'Login'}</button>
      </form>
    </div>
  )
}
