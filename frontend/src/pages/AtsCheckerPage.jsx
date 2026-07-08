import { useState } from 'react'
import FormShell from '../components/FormShell'
import useApiMutation from '../hooks/useApiMutation'

export default function AtsCheckerPage() {
  const [resume, setResume] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const mutation = useApiMutation('/ats/check')

  return (
    <FormShell title="ATS Checker">
      <textarea value={resume} onChange={(e) => setResume(e.target.value)} rows={6} className="mb-2 w-full rounded border p-2 bg-transparent" placeholder="Resume text" />
      <textarea value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} rows={6} className="w-full rounded border p-2 bg-transparent" placeholder="Job description" />
      <button onClick={() => mutation.mutate({ resume_text: resume, job_description: jobDescription })} className="mt-2 rounded bg-indigo-600 px-4 py-2 text-white">Check Match</button>
      {mutation.data && <pre className="mt-3 overflow-auto rounded bg-slate-100 p-2 text-xs dark:bg-slate-800">{JSON.stringify(mutation.data, null, 2)}</pre>}
    </FormShell>
  )
}
