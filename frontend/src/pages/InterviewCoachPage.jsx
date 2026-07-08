import { useState } from 'react'
import FormShell from '../components/FormShell'
import useApiMutation from '../hooks/useApiMutation'

export default function InterviewCoachPage() {
  const questionMutation = useApiMutation('/interview/questions')
  const evalMutation = useApiMutation('/interview/evaluate')
  const [setup, setSetup] = useState({ company: 'Google', mode: 'preset', round_type: 'technical' })
  const [answer, setAnswer] = useState('')

  return (
    <FormShell title="AI Interview Coach">
      <div className="grid gap-2 sm:grid-cols-3">
        <input className="rounded border p-2 bg-transparent" value={setup.company} onChange={(e) => setSetup({ ...setup, company: e.target.value })} />
        <select className="rounded border p-2 bg-transparent" value={setup.mode} onChange={(e) => setSetup({ ...setup, mode: e.target.value })}><option>preset</option><option>custom</option></select>
        <select className="rounded border p-2 bg-transparent" value={setup.round_type} onChange={(e) => setSetup({ ...setup, round_type: e.target.value })}>{['HR', 'technical', 'managerial', 'behavioral', 'system design'].map((v) => <option key={v}>{v}</option>)}</select>
      </div>
      <button className="mt-2 rounded bg-indigo-600 px-4 py-2 text-white" onClick={() => questionMutation.mutate(setup)}>Generate Questions</button>
      {questionMutation.data && <ul className="mt-2 list-disc pl-5 text-sm">{questionMutation.data.questions.map((q) => <li key={q}>{q}</li>)}</ul>}
      <textarea rows={4} className="mt-3 w-full rounded border p-2 bg-transparent" value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Type your answer to evaluate" />
      <button className="mt-2 rounded bg-emerald-600 px-4 py-2 text-white" onClick={() => evalMutation.mutate({ question: questionMutation.data?.questions?.[0] || '', answer })}>Evaluate Answer</button>
      {evalMutation.data && <pre className="mt-2 rounded bg-slate-100 p-2 text-xs dark:bg-slate-800">{JSON.stringify(evalMutation.data, null, 2)}</pre>}
    </FormShell>
  )
}
