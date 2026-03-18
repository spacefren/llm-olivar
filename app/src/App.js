import { useState } from 'react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setAnswer('');

    const q = question.trim();
    if (!q) {
      setError('Escribe una pregunta antes de enviar.');
      return;
    }

    try {
      setLoading(true);
      const res = await fetch('/api/mensaje', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensaje: q }),
      });

      if (!res.ok) {
        throw new Error(`Error HTTP ${res.status}`);
      }

      const data = await res.json();
      const texto = (data && data.respuesta) || 'Sin respuesta del servidor.';
      setAnswer(String(texto));
    } catch (err) {
      setError(
        err instanceof Error
          ? `No se ha podido contactar con el backend: ${err.message}`
          : 'No se ha podido contactar con el backend.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      className="App"
      style={{
        minHeight: '100vh',
        display: 'grid',
        placeItems: 'center',
        background: '#0f172a',
      }}
    >
      <main
        style={{
          width: 'min(720px, 92vw)',
          textAlign: 'left',
        }}
      >
        <div
          style={{
            background: '#111827',
            borderRadius: 16,
            padding: 20,
            boxShadow: '0 18px 40px rgba(0,0,0,0.45)',
            border: '1px solid rgba(148,163,184,0.35)',
          }}
        >
          <h1 style={{ margin: 0, fontSize: '1.8rem', color: '#e5e7eb' }}>OlivaIA</h1>
          <p style={{ marginTop: 8, opacity: 0.8, color: '#9ca3af' }}>
            Haz una pregunta sobre tu parcela y la IA irá completando los datos necesarios.
          </p>

          <form
            onSubmit={handleSubmit}
            style={{
              marginTop: 18,
              display: 'flex',
              gap: 10,
              alignItems: 'stretch',
            }}
          >
            <input
              type="text"
              placeholder="Escribe tu pregunta…"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading}
              style={{
                flex: 1,
                padding: '12px 14px',
                borderRadius: 10,
                border: '1px solid #d1d5db',
                background: '#ffffff',
                color: '#111827',
                outline: 'none',
              }}
            />
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '12px 14px',
                borderRadius: 10,
                border: 'none',
                background: loading ? '#9ca3af' : '#4b9c3f',
                color: 'white',
                cursor: loading ? 'default' : 'pointer',
                minWidth: 90,
              }}
            >
              {loading ? 'Enviando…' : 'Enviar'}
            </button>
          </form>

          <div
            style={{
              marginTop: 16,
              padding: 14,
              borderRadius: 12,
              border: '1px solid rgba(156,163,175,0.4)',
              background: '#020617',
              opacity: 0.95,
              whiteSpace: 'pre-wrap',
              color: '#e5e7eb',
              minHeight: 80,
            }}
          >
            {error && (
              <div style={{ color: '#fecaca', marginBottom: 6 }}>
                {error}
              </div>
            )}
            {answer || (!error && !loading && 'Aquí aparecerá la respuesta.')}
            {loading && !error && 'Consultando al modelo…'}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
