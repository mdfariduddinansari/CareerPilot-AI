export default function FormShell({ title, children }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <h1 className="mb-3 text-xl font-bold">{title}</h1>
      {children}
    </div>
  )
}
