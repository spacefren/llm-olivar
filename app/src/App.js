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
    <div className="App" style={{ minHeight: '100vh', display: 'grid', placeItems: 'center' }}>
      <main style={{ width: 'min(720px, 92vw)', textAlign: 'left' }}>
        <h1 style={{ margin: 0, fontSize: '1.8rem' }}>OlivaIA</h1>
        <p style={{ marginTop: 8, opacity: 0.8 }}>
          Haz una pregunta y el backend (stub) responderá.
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
              border: '1px solid rgba(255,255,255,.15)',
              background: 'rgba(255,255,255,.06)',
              color: 'white',
              outline: 'none',
            }}
          />
          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '12px 14px',
              borderRadius: 10,
              border: '1px solid rgba(255,255,255,.18)',
              background: loading ? 'rgba(124,170,45,.10)' : 'rgba(124,170,45,.25)',
              color: 'white',
              cursor: loading ? 'default' : 'pointer',
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
            border: '1px solid rgba(255,255,255,.10)',
            background: 'rgba(0,0,0,.22)',
            opacity: 0.9,
            whiteSpace: 'pre-wrap',
          }}
        >
          {error && (
            <div style={{ color: '#f8a5a5', marginBottom: 6 }}>
              {error}
            </div>
          )}
          {answer || (!error && !loading && 'Aquí aparecerá la respuesta.')}
          {loading && !error && 'Consultando al modelo…'}
        </div>
      </main>
    </div>
  );
}

export default App;
