import React, { useEffect, useState } from 'react'
import { getStats, getLogs, getAlerts } from '../api/client.js'

function Dashboard() {
  const [stats, setStats] = useState({})
  const [logs, setLogs] = useState([])
  const [alerts, setAlerts] = useState([])

  const refresh = async () => {
    try {
      const [s, l, a] = await Promise.all([getStats(), getLogs({ limit: 20 }), getAlerts()])
      setStats(s.data)
      setLogs(l.data)
      setAlerts(a.data)
    } catch (err) {
      console.error('API error', err)
    }
  }

  useEffect(() => {
    refresh()
    const id = setInterval(refresh, 5000) // Real-time polling
    return () => clearInterval(id)
  }, [])

  return (
    <div>
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <StatCard label="Total Logs" value={stats.total_logs} />
        <StatCard label="Open Alerts" value={stats.open_alerts} />
        <StatCard label="Critical" value={stats.critical_alerts} />
      </div>

      <h2>Alerts</h2>
      <ul>
        {alerts.map(a => (
          <li key={a.id} style={{ color: a.severity === 'high' ? '#ff7b72' : '#c9d1d9' }}>
            [{a.severity}] {a.title} - {a.source_ip}
          </li>
        ))}
      </ul>

      <h2>Recent Logs</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left' }}>Time</th>
            <th style={{ textAlign: 'left' }}>Source</th>
            <th style={{ textAlign: 'left' }}>IP</th>
            <th style={{ textAlign: 'left' }}>Message</th>
          </tr>
        </thead>
        <tbody>
          {logs.map(l => (
            <tr key={l.id} style={{ borderTop: '1px solid #30363d' }}>
              <td>{new Date(l.timestamp).toLocaleTimeString()}</td>
              <td>{l.source}</td>
              <td>{l.ip_address}</td>
              <td>{l.message}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function StatCard({ label, value }) {
  return (
    <div style={{ background: '#161b22', padding: '15px', borderRadius: '8px', minWidth: '120px' }}>
      <div style={{ fontSize: '12px', color: '#8b949e' }}>{label}</div>
      <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{value || 0}</div>
    </div>
  )
}

export default Dashboard
