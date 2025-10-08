import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchSummary } from '../api'

export default function Results() {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    (async () => {
      try {
        const res = await fetchSummary(id)
        setData(res)
      } catch (e) {
        setError('Failed to load results')
      } finally {
        setLoading(false)
      }
    })()
  }, [id])

  if (loading) return <p>Loading…</p>
  if (error) return <p className="text-red-600">{error}</p>
  if (!data) return null

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <h2 className="text-lg font-semibold mb-2">Transcript</h2>
        <pre className="whitespace-pre-wrap text-sm leading-relaxed">{data.transcript}</pre>
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        <div className="card p-4">
          <h3 className="font-semibold mb-2">Overview</h3>
          <p className="text-sm text-gray-700">{data.summary?.overview}</p>
        </div>
        <div className="card p-4">
          <h3 className="font-semibold mb-2">Decisions</h3>
          <ul className="text-sm list-disc pl-5 space-y-1">
            {data.summary?.decisions?.map((d, i) => <li key={i}>{d}</li>)}
          </ul>
        </div>
        <div className="card p-4">
          <h3 className="font-semibold mb-2">Action Items</h3>
          <ul className="text-sm list-disc pl-5 space-y-1">
            {data.summary?.action_items?.map((a, i) => <li key={i}>{a}</li>)}
          </ul>
        </div>
      </div>
    </div>
  )
}
