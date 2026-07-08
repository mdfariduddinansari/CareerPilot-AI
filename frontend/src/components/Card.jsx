export default function Card({ title, value, subtitle }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <p className="text-sm text-slate-500">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
      {subtitle ? <p className="text-xs text-slate-400">{subtitle}</p> : null}
    </div>
  )
}
