import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [activePage, setActivePage] = useState("analyze");

  useEffect(() => {
    // Load scan history from localStorage when the app opens
    const savedHistory = localStorage.getItem("scanHistory");

    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
  }, []);

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

      const newScan = {
        id: Date.now(),
        text: text,
        inputType: data.input_type,
        result: data.result,
        risk: data.risk,
        score: data.score,
        date: new Date().toLocaleString(),
      };

      const updatedHistory = [newScan, ...history];

      setHistory(updatedHistory);

      localStorage.setItem(
        "scanHistory",
        JSON.stringify(updatedHistory)
      );

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

          <div className="shield-icon">
            🛡
          </div>

          <div>
            <h2>PhishGuard</h2>
            <p>AI Security Scanner</p>
          </div>

        </div>

        <nav className="sidebar-nav">

          <button
            className={`nav-item ${
              activePage === "analyze" ? "active" : ""
            }`}
            onClick={() => setActivePage("analyze")}
          >
            <span>⌕</span>
            Analyze
          </button>

          <button
            className={`nav-item ${
              activePage === "history" ? "active" : ""
            }`}
            onClick={() => setActivePage("history")}
          >
            <span>◷</span>
            Scan History
          </button>

          <button className={`nav-item ${activePage === "about" ? "active" : ""
            }`}
              onClick={() => setActivePage("about")}
            >
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

          {/* SCAN HISTORY PAGE */}

          {activePage === "history" && (
            <section className="history-page">

              <header className="page-header">

                    <div className="history-header">

                      <div>

                        <span className="eyebrow">
                          PREVIOUS SCANS
                        </span>

                        <h1>
                          Scan History
                        </h1>

                        <p>
                          View your previously analyzed emails, URLs, and messages.
                        </p>

                      </div>

                      {history.length > 0 && (
                        <button
                          className="clear-history-button"
                          onClick={() => {
                            setHistory([]);
                            localStorage.removeItem("scanHistory");
                          }}
                        >
                          Clear History
                        </button>
                      )}

                    </div>

</header>

              {history.length === 0 ? (

                <section className="scanner-card">

                  <h2>
                    No scans yet
                  </h2>

                  <p>
                    Your completed scans will appear here.
                  </p>

                </section>

              ) : (

                <div className="history-list">

                  {history.map((scan) => (

                    <article
                      className="history-card"
                      key={scan.id}
                    >

                      <div className="history-card-header">

                        <div>

                          <span className="result-label">
                            {scan.inputType}
                          </span>

                          <h3>
                            {scan.result}
                          </h3>

                        </div>

                        <span
                          className={`risk-badge risk-${scan.risk.toLowerCase()}`}
                        >
                          {scan.risk}
                        </span>

                      </div>

                      <p className="history-text">
                        {scan.text}
                      </p>

                      <div className="history-details">

                        <span>
                          Score: {scan.score}/100
                        </span>

                        <span>
                          {scan.date}
                        </span>

                      </div>

                    </article>

                  ))}

                </div>

              )}

            </section>
          )}

          {/* ANALYZE PAGE */}

          {activePage === "about" && (
  <section className="about-page">

    <header className="page-header">

      <span className="eyebrow">
        ABOUT PHISHGUARD
      </span>

      <h1>
        Security awareness powered by AI.
      </h1>

      <p>
        PhishGuard analyzes suspicious emails, URLs, and messages
        to help users identify possible phishing threats.
      </p>

    </header>

    <section className="about-card">

      <h2>
        How PhishGuard works
      </h2>

      <p>
        The application combines machine-learning predictions,
        rule-based security checks, and URL reputation analysis
        to evaluate potentially malicious content.
      </p>

      <div className="about-features">

        <article className="about-feature">

          <div className="about-icon">
            🧠
          </div>

          <h3>
            Machine Learning
          </h3>

          <p>
            An AI model analyzes patterns associated with
            phishing and legitimate content.
          </p>

        </article>

        <article className="about-feature">

          <div className="about-icon">
            🔍
          </div>

          <h3>
            Threat Detection
          </h3>

          <p>
            Security rules check for urgency, credential requests,
            suspicious links, and impersonation indicators.
          </p>

        </article>

        <article className="about-feature">

          <div className="about-icon">
            📊
          </div>

          <h3>
            Risk Assessment
          </h3>

          <p>
            Scan results provide a risk level, score, confidence,
            and explanations for the detection.
          </p>

        </article>

      </div>

    </section>

    <section className="security-notice">

      <div className="security-notice-icon">
        🛡
      </div>

      <div>

        <h3>
          Important security notice
        </h3>

        <p>
          PhishGuard provides automated security assessments.
          Results should support—not replace—careful judgment
          when handling suspicious content.
        </p>

      </div>

    </section>

  </section>
)}

          {activePage === "analyze" && (
            <>

              <header className="page-header">

                <span className="eyebrow">
                  AI-POWERED SECURITY
                </span>

                <h1>
                  Detect phishing before it causes damage.
                </h1>

                <p>
                  Paste an email, URL, or SMS message.
                  Our detection engine analyzes suspicious
                  indicators and provides a risk assessment.
                </p>

              </header>

              <section className="scanner-card">

                <label htmlFor="scanner-input">
                  Content to analyze
                </label>

                <textarea
                  id="scanner-input"
                  value={text}
                  onChange={(event) =>
                    setText(event.target.value)
                  }
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

                      <h2>
                        Analysis Result
                      </h2>

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

                      result.reasons.map(
                        (reason, index) => (

                          <li key={index}>
                            {reason}
                          </li>

                        )
                      )

                    ) : (

                      <li>
                        No suspicious indicators were found.
                      </li>

                    )}

                  </ul>

                </section>

              )}

            </>
          )}

        </div>

      </main>

    </div>
  );
}

export default App;