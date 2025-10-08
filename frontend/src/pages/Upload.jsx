import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { uploadFile } from '../api'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const onSubmit = async (e) => {
    e.preventDefault()
    setError('')
    if (!file) { setError('Please select an audio file (.mp3, .wav, .mp4)'); return }
    setLoading(true)
    try {
      const data = await uploadFile(file)
      navigate(`/results/${data._id}`)
    } catch (err) {
      console.error(err)
      setError('Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-primary-700 to-accent-700 bg-clip-text text-transparent">
          Upload & Transcribe
        </h1>
        <p className="text-gray-600">Transform your meeting recordings into actionable insights</p>
      </div>

      <div className="card p-8">
        <form onSubmit={onSubmit} className="space-y-6">
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              Select Audio File
            </label>
            <input
              type="file"
              accept=".mp3,.wav,.mp4"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="file-input"
            />
            {file && (
              <div className="flex items-center gap-2 text-sm text-primary-700 bg-primary-50 px-4 py-2 rounded-lg">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="font-medium">{file.name}</span>
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Upload & Transcribe
              </>
            )}
          </button>
        </form>
        {error && (
          <div className="mt-4 flex items-center gap-2 text-sm text-red-600 bg-red-50 px-4 py-3 rounded-lg">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {error}
          </div>
        )}
      </div>

      <div className="flex items-center justify-center gap-6 text-sm text-gray-500">
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <span>MP3, WAV, MP4</span>
        </div>
        <div className="flex items-center gap-2">
          <svg className="w-4 h-4 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <span>AI-Powered</span>
        </div>
      </div>
    </div>
  )
}
