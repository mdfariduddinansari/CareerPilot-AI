import { useState } from 'react'
import FormShell from '../components/FormShell'
import useApiMutation from '../hooks/useApiMutation'
import { exportTextPdf } from '../utils/pdf'

export default function CoverLetterPage() {
  const mutation = useApiMutation('/cover-letter/generate')
  const [form, setForm] = useState({ company: '', role: '', tone: 'professional', resume_text: '' })

  return (
    <FormShell title="AI Cover Letter Generator">
      <div className="grid gap-2 sm:grid-cols-2">
        <input className="rounded border p-2 bg-transparent" placeholder="Company" value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} />
        <input className="rounded border p-2 bg-transparent" placeholder="Role" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} />
      </div>
      <select className="mt-2 rounded border p-2 bg-transparent" value={form.tone} onChange={(e) => setForm({ ...form, tone: e.target.value })}>
        {['professional', 'friendly', 'startup', 'corporate', 'creative'].map((tone) => <option key={tone}>{tone}</option>)}
      </select>
      <textarea className="mt-2 w-full rounded border p-2 bg-transparent" rows={6} placeholder="Resume text" value={form.resume_text} onChange={(e) => setForm({ ...form, resume_text: e.target.value })} />
      <button className="mt-2 rounded bg-indigo-600 px-4 py-2 text-white" onClick={() => mutation.mutate(form)}>Generate</button>
      {mutation.data && (
        <div className="mt-3">
          <textarea rows={10} className="w-full rounded border p-2 bg-transparent" value={mutation.data.letter} readOnly />
          <button className="mt-2 rounded bg-slate-800 px-3 py-1 text-white" onClick={() => exportTextPdf('Cover Letter', mutation.data.letter)}>Export PDF</button>
        </div>
      )}
    </FormShell>
  )
}
