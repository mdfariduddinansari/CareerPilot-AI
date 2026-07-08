import { Link, Outlet } from 'react-router-dom'
import Navbar from '../components/Navbar'

const navItems = [
  ['/', 'Dashboard'],
  ['/resume-analyzer', 'Resume Analyzer'],
  ['/ats-checker', 'ATS Checker'],
  ['/cover-letter', 'Cover Letter'],
  ['/interview-coach', 'Interview Coach'],
  ['/linkedin-post', 'LinkedIn Post'],
  ['/job-tracker', 'Job Tracker'],
  ['/skill-gap', 'Skill Gap']
]

export default function DashboardLayout() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <div className="mx-auto flex max-w-7xl gap-4 p-4">
        <aside className="hidden w-56 rounded-xl border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-900 md:block">
          {navItems.map(([to, label]) => (
            <Link key={to} to={to} className="mb-1 block rounded-md px-3 py-2 text-sm hover:bg-slate-100 dark:hover:bg-slate-800">
              {label}
            </Link>
          ))}
        </aside>
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
