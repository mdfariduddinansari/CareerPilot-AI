import { useQuery } from '@tanstack/react-query'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { motion } from 'framer-motion'
import api from '../services/api'
import Card from '../components/Card'

export default function DashboardPage() {
  const { data } = useQuery({
    queryKey: ['summary'],
    queryFn: async () => (await api.get('/dashboard/summary')).data.data
  })

  const cards = data?.cards || []
  const chartData = data?.applications_by_stage || []

  return (
    <div className="space-y-4">
      <motion.h1 initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="text-2xl font-bold">
        Mission Control Dashboard
      </motion.h1>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((card) => <Card key={card.title} {...card} />)}
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
        <h2 className="mb-2 font-semibold">Applications by Stage</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <XAxis dataKey="stage" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#6366f1" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
