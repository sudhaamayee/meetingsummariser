import { Outlet, Link, useLocation } from 'react-router-dom'

export default function App() {
  const { pathname } = useLocation()
  return (
    <div className="min-h-screen">
      <header className="bg-white/70 backdrop-blur-md border-b border-primary-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-accent-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-lg">📄</span>
            </div>
            <span className="font-bold text-xl bg-gradient-to-r from-primary-700 to-accent-700 bg-clip-text text-transparent">SummarIQ</span>
          </Link>
          <nav className="flex gap-2">
            <Link 
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                pathname==='/' 
                  ? 'bg-primary-100 text-primary-700' 
                  : 'text-gray-600 hover:bg-primary-50 hover:text-primary-600'
              }`} 
              to="/"
            >
              Upload
            </Link>
            <Link 
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                pathname.startsWith('/history') 
                  ? 'bg-primary-100 text-primary-700' 
                  : 'text-gray-600 hover:bg-primary-50 hover:text-primary-600'
              }`} 
              to="/history"
            >
              History
            </Link>
          </nav>
        </div>
      </header>
      <main className="max-w-5xl mx-auto px-6 py-12">
        <Outlet />
      </main>
      <footer className="text-center text-sm text-gray-500 py-8 border-t border-primary-100">
        <p>Built with <span className="text-primary-600 font-medium">FastAPI</span> + <span className="text-primary-600 font-medium">React</span></p>
      </footer>
    </div>
  )
}
