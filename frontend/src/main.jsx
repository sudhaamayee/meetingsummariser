import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import App from './App'
import Upload from './pages/Upload'
import Results from './pages/Results'
import History from './pages/History'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Upload /> },
      { path: 'results/:id', element: <Results /> },
      { path: 'history', element: <History /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
