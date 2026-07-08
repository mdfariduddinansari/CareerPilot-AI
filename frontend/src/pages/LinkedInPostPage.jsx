import { useState } from 'react'
import FormShell from '../components/FormShell'
import useApiMutation from '../hooks/useApiMutation'

export default function LinkedInPostPage() {
  const [form, setForm] = useState({ post_type: 'project showcase', tone: 'professional', context: '' })
  const mutation = useApiMutation('/linkedin/generate')

  return (
    <FormShell title="LinkedIn Post Generator">
      <div className="grid gap-2 sm:grid-cols-2">
        <select className="rounded border p-2 bg-transparent" value={form.post_type} onChange={(e) => setForm({ ...form, post_type: e.target.value })}>{['internship', 'placement', 'project showcase', 'hackathon', 'achievement', 'open to work', 'branding'].map((v) => <option key={v}>{v}</option>)}</select>
        <input className="rounded border p-2 bg-transparent" value={form.tone} onChange={(e) => setForm({ ...form, tone: e.target.value })} placeholder="Tone" />
      </div>
      <textarea className="mt-2 w-full rounded border p-2 bg-transparent" rows={5} value={form.context} onChange={(e) => setForm({ ...form, context: e.target.value })} placeholder="What should the post mention?" />
      <button className="mt-2 rounded bg-indigo-600 px-4 py-2 text-white" onClick={() => mutation.mutate(form)}>Generate Variants</button>
      {mutation.data && <ol className="mt-2 list-decimal pl-5 text-sm">{mutation.data.variants.map((v) => <li key={v}>{v}</li>)}</ol>}
    </FormShell>
  )
}
