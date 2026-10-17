import { useState } from 'react'

const API = 'http://localhost:8000'

export default function App() {
  const [iterations, setIterations] = useState(100)
  const [particles, setParticles] = useState(30)
  const [seed, setSeed] = useState(42)
  const [status, setStatus] = useState('idle')
  const [result, setResult] = useState(null)
  const [runId, setRunId] = useState(null)

  const busy = status === 'pending' || status === 'running'

  async function run() {
    setStatus('pending')
    setResult(null)
    setRunId(null)
    try {
      const res = await fetch(`${API}/api/opt/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          optimizer: {
            name: 'pso',
            config: { iterations, particles, seed },
          },
        }),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setRunId(data.run_id)
      poll(data.run_id)
    } catch (err) {
      setStatus('failed')
      setResult({ error: String(err) })
    }
  }

  async function poll(id) {
    try {
      const res = await fetch(`${API}/api/opt/runs/${id}/result`)
      const data = await res.json()
      setStatus(data.status)
      if (data.status === 'completed' || data.status === 'failed') {
        setResult(data.result)
      } else {
        setTimeout(() => poll(id), 500)
      }
    } catch (err) {
      setStatus('failed')
      setResult({ error: String(err) })
    }
  }

  return (
    <div className="container">
      <header>
        <h1>OptiLab</h1>
        <p className="subtitle">
          Extensible Optimization Playground — demo: PSO on the Rastrigin function
        </p>
      </header>

      <section className="controls">
        <label>
          Iterations
          <input
            type="number"
            min="1"
            value={iterations}
            onChange={(e) => setIterations(Number(e.target.value))}
          />
        </label>
        <label>
          Particles
          <input
            type="number"
            min="1"
            value={particles}
            onChange={(e) => setParticles(Number(e.target.value))}
          />
        </label>
        <label>
          Seed
          <input
            type="number"
            value={seed}
            onChange={(e) => setSeed(Number(e.target.value))}
          />
        </label>
        <button onClick={run} disabled={busy}>
          {busy ? 'Running…' : 'Run PSO'}
        </button>
      </section>

      <section className="status">
        <p>
          Status: <strong>{status}</strong>
          {runId && <span className="run-id"> ({runId.slice(0, 8)}…)</span>}
        </p>
      </section>

      {result && result.best_value !== undefined && (
        <section className="result">
          <p>
            Best value: <strong>{result.best_value.toFixed(6)}</strong>
          </p>
          <p>
            Best position:{' '}
            <code>[{result.best_position.map((v) => v.toFixed(4)).join(', ')}]</code>
          </p>
          <p>Iterations recorded: {result.history?.length ?? 0}</p>
        </section>
      )}

      {result?.error && (
        <section className="error">
          <p>Error: {result.error}</p>
        </section>
      )}
    </div>
  )
}
