import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchHistory } from '../api'

export default function History() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    (async () => {
      const res = await fetchHistory()
      setItems(res)
      setLoading(false)
    })()
  }, [])

  if (loading) return <p>Loading…</p>

  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold mb-4">History</h2>
      <ul className="divide-y">
        {items.map(item => (
          <li key={item._id} className="py-3 flex items-center justify-between">
            <div>
              <p className="font-medium text-sm">{item.filename}</p>
              <p className="text-xs text-gray-500">{new Date(item.createdAt).toLocaleString()}</p>
            </div>
            <Link className="text-sm text-blue-600" to={`/results/${item._id}`}>View</Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
