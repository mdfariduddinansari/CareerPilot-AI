import { useState } from 'react'
import FormShell from '../components/FormShell'
import useApiMutation from '../hooks/useApiMutation'
import { exportTextPdf } from '../utils/pdf'

export default function SkillGapPage() {
  const [targetRole, setTargetRole] = useState('Software Engineer')
  const [skills, setSkills] = useState('Python, React')
  const mutation = useApiMutation('/skills/analyze')

  return (
    <FormShell title="Skill Gap Analyzer + Learning Roadmap">
      <input className="mb-2 w-full rounded border p-2 bg-transparent" value={targetRole} onChange={(e) => setTargetRole(e.target.value)} placeholder="Target role" />
      <input className="w-full rounded border p-2 bg-transparent" value={skills} onChange={(e) => setSkills(e.target.value)} placeholder="Current skills comma separated" />
      <button className="mt-2 rounded bg-indigo-600 px-4 py-2 text-white" onClick={() => mutation.mutate({ target_role: targetRole, current_skills: skills.split(',').map((x) => x.trim()).filter(Boolean) })}>Analyze</button>
      {mutation.data && (
        <div className="mt-2 text-sm">
          <pre className="overflow-auto rounded bg-slate-100 p-2 text-xs dark:bg-slate-800">{JSON.stringify(mutation.data, null, 2)}</pre>
          <button className="mt-2 rounded bg-slate-800 px-3 py-1 text-white" onClick={() => exportTextPdf('Learning Roadmap', JSON.stringify(mutation.data.roadmap, null, 2))}>Export Roadmap PDF</button>
        </div>
      )}
    </FormShell>
  )
}
