import { Link } from 'react-router-dom'
import { useTheme } from '../context/ThemeContext'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { darkMode, toggleTheme } = useTheme()
  const { logout } = useAuth()

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3 dark:border-slate-800 dark:bg-slate-900">
      <Link to="/" className="text-lg font-bold text-indigo-600">CareerPilot AI</Link>
      <div className="flex gap-2">
        <button onClick={toggleTheme} className="rounded-md bg-slate-100 px-3 py-1 text-sm dark:bg-slate-800">
          {darkMode ? 'Light' : 'Dark'}
        </button>
        <button onClick={logout} className="rounded-md bg-indigo-600 px-3 py-1 text-sm text-white">Logout</button>
      </div>
    </header>
  )
}
