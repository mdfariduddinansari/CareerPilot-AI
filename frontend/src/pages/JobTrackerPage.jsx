import { useEffect, useState } from 'react'
import api from '../services/api'
import FormShell from '../components/FormShell'

const columns = ['Wishlist', 'Applied', 'OA', 'Interview', 'Offer', 'Rejected']

export default function JobTrackerPage() {
  const [jobs, setJobs] = useState([])
  const [newJob, setNewJob] = useState({ company: '', role: '' })

  const load = async () => {
    const { data } = await api.get('/jobs')
    setJobs(data.data)
  }

  useEffect(() => { load() }, [])

  const createJob = async () => {
    await api.post('/jobs', { ...newJob, status: 'Wishlist' })
    setNewJob({ company: '', role: '' })
    load()
  }

  const onDrop = async (jobId, status) => {
    await api.patch(`/jobs/${jobId}`, { status })
    load()
  }

  return (
    <FormShell title="Job Tracker">
      <div className="mb-3 flex gap-2">
        <input className="rounded border p-2 bg-transparent" placeholder="Company" value={newJob.company} onChange={(e) => setNewJob({ ...newJob, company: e.target.value })} />
        <input className="rounded border p-2 bg-transparent" placeholder="Role" value={newJob.role} onChange={(e) => setNewJob({ ...newJob, role: e.target.value })} />
        <button className="rounded bg-indigo-600 px-3 py-2 text-white" onClick={createJob}>Add</button>
      </div>
      <div className="grid gap-3 md:grid-cols-3 xl:grid-cols-6">
        {columns.map((column) => (
          <div key={column} onDragOver={(e) => e.preventDefault()} onDrop={(e) => onDrop(e.dataTransfer.getData('jobId'), column)} className="min-h-44 rounded-lg border border-slate-200 p-2 dark:border-slate-800">
            <h3 className="mb-2 text-sm font-semibold">{column}</h3>
            {jobs.filter((job) => job.status === column).map((job) => (
              <div key={job.id} draggable onDragStart={(e) => e.dataTransfer.setData('jobId', String(job.id))} className="mb-2 rounded bg-slate-100 p-2 text-xs dark:bg-slate-800">
                <p className="font-semibold">{job.company}</p>
                <p>{job.role}</p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </FormShell>
  )
}
