import { useState } from 'react';

export default function Home() {
  const [apiKey, setApiKey] = useState('');
  const [developerMessage, setDeveloperMessage] = useState('');
  const [userMessage, setUserMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([
    // Optionally, start with the system/developer message
    // { role: "system", content: developerMessage }
  ]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setResponse('');

    // Build the full message history
    const messages = [
      { role: "system", content: developerMessage },
      ...history,
      { role: "user", content: userMessage }
    ];

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages,
        api_key: apiKey,
      }),
    });

    if (!res.body) {
      setLoading(false);
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let done = false;
    let assistantReply = '';
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      if (value) {
        const chunk = decoder.decode(value);
        setResponse((prev) => prev + chunk);
        assistantReply += chunk;
      }
    }
    setLoading(false);

    // Update history with the new user message and assistant reply
    setHistory([
      ...history,
      { role: "user", content: userMessage },
      { role: "assistant", content: assistantReply }
    ]);
  }

  return (
    <main className="container">
      <h1>AI Engineer Chat</h1>
      <form onSubmit={handleSubmit}>
        <label>
          API Key
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            required
          />
        </label>
        <label>
          Developer Message
          <textarea
            value={developerMessage}
            onChange={(e) => setDeveloperMessage(e.target.value)}
            required
          />
        </label>
        <label>
          User Message
          <textarea
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={loading}>Send</button>
      </form>
      <div className="history">
        {history.map((msg, idx) => (
          <div key={idx} className={msg.role}>
            <b>{msg.role}:</b> {msg.content}
          </div>
        ))}
      </div>
      <style jsx>{`
        .container {
          padding: 2rem;
          color: #fff;
          background: #111;
          min-height: 100vh;
          font-family: monospace;
        }
        label {
          display: block;
          margin-bottom: 1rem;
        }
        input, textarea {
          width: 100%;
          padding: 0.5rem;
          margin-top: 0.25rem;
          border-radius: 4px;
          border: 1px solid #333;
          background: #000;
          color: #fff;
        }
        button {
          background: #ff0080;
          border: none;
          color: #fff;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          cursor: pointer;
        }
        button:disabled {
          opacity: 0.6;
        }
        .history {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin-top: 2rem;
        }
        .user {
          align-self: flex-end;
          background: #222;
          color: #fff;
          border-radius: 8px;
          padding: 0.5rem 1rem;
          max-width: 70%;
        }
        .assistant {
          align-self: flex-start;
          background: #333;
          color: #fff;
          border-radius: 8px;
          padding: 0.5rem 1rem;
          max-width: 70%;
        }
      `}</style>
    </main>
  );
}

