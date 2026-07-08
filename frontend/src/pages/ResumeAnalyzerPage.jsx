import { useState } from 'react'
import FormShell from '../components/FormShell'
import useApiMutation from '../hooks/useApiMutation'
import { exportTextPdf } from '../utils/pdf'

export default function ResumeAnalyzerPage() {
  const [resumeText, setResumeText] = useState('')
  const mutation = useApiMutation('/resume/analyze')

  return (
    <FormShell title="AI Resume Analyzer">
      <textarea value={resumeText} onChange={(e) => setResumeText(e.target.value)} rows={8} className="w-full rounded border p-2 bg-transparent" placeholder="Paste your resume text" />
      <button onClick={() => mutation.mutate({ resume_text: resumeText })} className="mt-2 rounded bg-indigo-600 px-4 py-2 text-white">Analyze</button>
      {mutation.data && (
        <div className="mt-4 space-y-2 text-sm">
          <p><strong>Overall:</strong> {mutation.data.overall_score}% | <strong>ATS:</strong> {mutation.data.ats_score}%</p>
          <p><strong>Suggestions:</strong> {mutation.data.suggestions.join(', ')}</p>
          <button className="rounded bg-slate-800 px-3 py-1 text-white" onClick={() => exportTextPdf('Resume Report', JSON.stringify(mutation.data, null, 2))}>Export PDF</button>
        </div>
      )}
    </FormShell>
  )
}
