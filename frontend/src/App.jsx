import Dashboard from './components/Dashboard.jsx'

function App() {
  return (
    <div style={{ fontFamily: 'monospace', padding: '20px', background: '#0d1117', color: '#c9d1d9', minHeight: '100vh' }}>
      <h1>Mini SIEM Platform</h1>
      <Dashboard />
    </div>
  )
}

export default App
