import React, { useRef, useState, useEffect } from "react";

export default function Home() {
  const [chat, setChat] = useState<any[]>([]);
  const [message, setMessage] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, loading]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() && !file) return;
    setLoading(true);
    setError("");
    setChat(prev => [
      ...prev,
      { role: "user", content: message, fileName: file?.name }
    ]);
    try {
      const formData = new FormData();
      formData.append("message", message);
      if (file) formData.append("file", file);
      const res = await fetch("/upload_and_ask", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Backend error");
      const data = await res.json();
      setChat(prev => [
        ...prev,
        { role: "assistant", content: data.answer, fileName: undefined }
      ]);
    } catch (err) {
      setError("Failed to get response from backend.");
    }
    setLoading(false);
    setMessage("");
    setFile(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div className="gpt-root">
      <main className="gpt-chat-area">
        <div className="gpt-chat-history">
          {chat.map((msg, idx) => (
            <div
              key={idx}
              className={`gpt-bubble ${msg.role}`}
            >
              {msg.fileName && (
                <div className="gpt-file-preview-inline">
                  <span className="gpt-file-icon">📄</span>
                  <span className="gpt-file-name">{msg.fileName}</span>
                </div>
              )}
              <span>{msg.content}</span>
            </div>
          ))}
          {loading && <div className="gpt-bubble assistant">AI is typing...</div>}
          <div ref={chatEndRef} />
        </div>
        <form className="gpt-input-card" onSubmit={handleSend}>
          {file && (
            <div className="gpt-file-preview">
              <span className="gpt-file-icon">📄</span>
              <span className="gpt-file-name">{file.name}</span>
              <button
                type="button"
                className="gpt-file-remove"
                onClick={() => setFile(null)}
                disabled={loading}
                aria-label="Remove file"
              >
                ❌
              </button>
            </div>
          )}
          <div className="gpt-input-row">
            <textarea
              className="gpt-input"
              value={message}
              onChange={e => setMessage(e.target.value)}
              placeholder="Ask anything..."
              disabled={loading}
              rows={1}
              style={{ resize: "none" }}
            />
            <label className="gpt-file-upload">
              <input
                type="file"
                accept=".pdf,.docx,.txt,.md"
                style={{ display: "none" }}
                onChange={handleFileChange}
                disabled={loading}
              />
              <span role="img" aria-label="Attach file">📎</span>
            </label>
            <button className="gpt-send-btn" type="submit" disabled={loading || (!message.trim() && !file)}>
              <span>&uarr;</span>
            </button>
          </div>
          {error && <div className="gpt-error">{error}</div>}
        </form>
      </main>
      <style jsx>{`
        .gpt-root {
          min-height: 100vh;
          background: #18181b;
          color: #f3f4f6;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: flex-start;
        }
        .gpt-chat-area {
          width: 100vw;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: flex-end;
          padding-top: 10vh;
        }
        .gpt-chat-history {
          width: 100%;
          max-width: 700px;
          flex: 1 1 0%;
          min-height: 0;
          margin: 0;
          padding: 2rem 1.5rem 1rem 1.5rem;
          overflow-y: auto;
          display: flex;
          flex-direction: column;
          background: #232329;
          border-radius: 1.5rem 1.5rem 0 0;
        }
        .gpt-bubble {
          margin-bottom: 1.2rem;
          padding: 1rem 1.25rem;
          border-radius: 1.25rem;
          max-width: 80%;
          word-break: break-word;
          font-size: 1rem;
          background: #27272a;
          color: #f3f4f6;
        }
        .gpt-bubble.user {
          align-self: flex-end;
          background: #3b3b41;
          color: #f3f4f6;
        }
        .gpt-bubble.assistant {
          align-self: flex-start;
          background: #232329;
          color: #f3f4f6;
        }
        .gpt-file-preview-inline {
          display: flex;
          align-items: center;
          background: #35353b;
          border-radius: 0.75rem;
          padding: 0.25rem 0.75rem;
          margin-bottom: 0.5rem;
          font-size: 0.95em;
        }
        .gpt-file-icon {
          font-size: 1.1em;
          margin-right: 0.5em;
        }
        .gpt-file-name {
          flex: 1;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          margin-right: 0.4em;
          font-size: 0.95em;
        }
        .gpt-input-card {
          background: #232329;
          border-radius: 0 0 1.5rem 1.5rem;
          box-shadow: 0 4px 32px 0 rgba(0,0,0,0.18);
          width: 100%;
          max-width: 700px;
          margin: 0 auto 0 auto;
          padding: 1.25rem 1.5rem 1rem 1.5rem;
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .gpt-file-preview {
          display: flex;
          align-items: center;
          background: #35353b;
          border-radius: 0.75rem;
          padding: 0.5rem 1rem;
          font-size: 0.95em;
          margin-bottom: 0.5rem;
        }
        .gpt-file-remove {
          background: none;
          border: none;
          color: #f87171;
          font-size: 1em;
          cursor: pointer;
          margin-left: 0.5em;
        }
        .gpt-input-row {
          display: flex;
          align-items: flex-end;
          gap: 0.75rem;
          width: 100%;
        }
        .gpt-input {
          border: 1.5px solid #35353b;
          outline: none;
          font-size: 1rem;
          background: #18181b;
          color: #f3f4f6;
          flex: 1;
          min-width: 0;
          border-radius: 1.5rem;
          padding: 1.1rem 1.25rem;
          transition: border 0.2s;
          min-height: 3.5rem;
          line-height: 1.5;
          resize: none;
          box-sizing: border-box;
        }
        .gpt-input:focus {
          border: 1.5px solid #6366f1;
          background: #232329;
        }
        .gpt-file-upload {
          cursor: pointer;
          font-size: 1.1rem;
          margin-left: 0.25rem;
        }
        .gpt-send-btn {
          background: linear-gradient(90deg, #f472b6, #818cf8);
          color: #fff;
          border: none;
          border-radius: 50%;
          width: 38px;
          height: 38px;
          font-size: 1.2rem;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          box-shadow: 0 2px 8px 0 rgba(0,0,0,0.08);
          transition: background 0.2s;
          margin-left: 0.5rem;
        }
        .gpt-send-btn:hover {
          background: linear-gradient(90deg, #818cf8, #f472b6);
        }
        .gpt-error {
          color: #f87171;
          font-size: 0.95em;
          margin-top: 0.5rem;
        }
        @media (max-width: 800px) {
          .gpt-chat-area, .gpt-chat-history, .gpt-input-card {
            max-width: 100vw;
            border-radius: 0;
          }
        }
        html, body, #__next, .gpt-root, .gpt-chat-area {
          height: 100vh;
        }
      `}</style>
    </div>
  );
} 