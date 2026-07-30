import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeText = async () => {
    if (!text.trim()) {
      setError("Please enter an email, URL, or message.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/analyze/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: text,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Analysis request failed.");
      }

      const data = await response.json();

      setResult(data);

    } catch (error) {
      setError(
        "Could not connect to the Django API. Make sure Django is running."
      );

    } finally {
      setLoading(false);
    }
  };


    return (
  <div className="app-layout">

    <aside className="sidebar">

      <div className="sidebar-brand">
        <div className="shield-icon">🛡</div>

        <div>
          <h2>PhishGuard</h2>
          <p>AI Security Scanner</p>
        </div>
      </div>

      <nav className="sidebar-nav">

        <button className="nav-item active">
          <span>⌕</span>
          Analyze
        </button>

        <button className="nav-item">
          <span>◷</span>
          Scan History
        </button>

        <button className="nav-item">
          <span>ⓘ</span>
          About
        </button>

      </nav>

      <div className="sidebar-footer">
        <span className="status-dot"></span>
        Detection system online
      </div>

    </aside>

    <main className="main-content">

      <div className="content-wrapper">

        <header className="page-header">

          <span className="eyebrow">
            AI-POWERED SECURITY
          </span>

          <h1>
            Detect phishing before it causes damage.
          </h1>

          <p>
            Paste an email, URL, or SMS message. Our detection engine
            analyzes suspicious indicators and provides a risk assessment.
          </p>

        </header>

        <section className="scanner-card">

          <label htmlFor="scanner-input">
            Content to analyze
          </label>

          <textarea
            id="scanner-input"
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Paste a suspicious email, URL, or SMS message here..."
            rows="10"
          />

          <button
            className="analyze-button"
            onClick={analyzeText}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              <>
                <span>🛡</span>
                Analyze Content
              </>
            )}
          </button>

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

        </section>

        {result && (
          <section className="result-card">

            <div className="result-heading">

              <div>
                <span className="eyebrow">
                  SCAN COMPLETE
                </span>

                <h2>Analysis Result</h2>
              </div>

              <span
                className={`risk-badge risk-${result.risk.toLowerCase()}`}
              >
                {result.risk}
              </span>

            </div>

            <div className="result-grid">

              <div className="result-item">
                <span className="result-label">
                  Input Type
                </span>

                <strong>
                  {result.input_type}
                </strong>
              </div>

              <div className="result-item">
                <span className="result-label">
                  Detection
                </span>

                <strong>
                  {result.result}
                </strong>
              </div>

              <div className="result-item">
                <span className="result-label">
                  Risk Score
                </span>

                <strong>
                  {result.score}/100
                </strong>
              </div>

              <div className="result-item">
                <span className="result-label">
                  Confidence
                </span>

                <strong>
                  {result.confidence}%
                </strong>
              </div>

            </div>

            <h3>
              Why was this result given?
            </h3>

            <ul className="reasons-list">

              {result.reasons.length > 0 ? (

                result.reasons.map((reason, index) => (

                  <li key={index}>
                    {reason}
                  </li>

                ))

              ) : (

                <li>
                  No suspicious indicators were found.
                </li>

              )}

            </ul>

          </section>
        )}

      </div>

    </main>

  </div>
);
}

export default App;