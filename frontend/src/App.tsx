import { FormEvent, useState } from "react";

import { ApiError, getHealth, postAsk, postIndex } from "./api";
import type { AskResponse, HealthResponse, IndexResponse } from "./types";

function App() {
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState(false);
  const [healthError, setHealthError] = useState<string | null>(null);

  const [inputDir, setInputDir] = useState("./sample_docs/text_only");
  const [indexPath, setIndexPath] = useState("./local_index.json");
  const [indexData, setIndexData] = useState<IndexResponse | null>(null);
  const [indexLoading, setIndexLoading] = useState(false);
  const [indexError, setIndexError] = useState<string | null>(null);

  const [query, setQuery] = useState("Where should billing questions be routed?");
  const [topK, setTopK] = useState(3);
  const [askData, setAskData] = useState<AskResponse | null>(null);
  const [askLoading, setAskLoading] = useState(false);
  const [askError, setAskError] = useState<string | null>(null);

  async function handleHealthCheck() {
    setHealthLoading(true);
    setHealthError(null);
    try {
      const response = await getHealth();
      setHealthData(response);
    } catch (error) {
      setHealthError(error instanceof Error ? error.message : "Unknown health request error");
      setHealthData(null);
    } finally {
      setHealthLoading(false);
    }
  }

  async function handleIndexSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setIndexLoading(true);
    setIndexError(null);
    try {
      const response = await postIndex({ input_dir: inputDir, index_path: indexPath });
      setIndexData(response);
    } catch (error) {
      if (error instanceof ApiError) {
        setIndexError(`Backend returned ${error.status}: ${error.detail}`);
      } else {
        setIndexError(error instanceof Error ? error.message : "Unknown index request error");
      }
      setIndexData(null);
    } finally {
      setIndexLoading(false);
    }
  }

  async function handleAskSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setAskLoading(true);
    setAskError(null);
    try {
      const response = await postAsk({ index_path: indexPath, query, top_k: topK });
      setAskData(response);
    } catch (error) {
      if (error instanceof ApiError) {
        setAskError(`Backend returned ${error.status}: ${error.detail}`);
      } else {
        setAskError(error instanceof Error ? error.message : "Unknown ask request error");
      }
      setAskData(null);
    } finally {
      setAskLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="hero">
        <h1>Grounded RAG Assistant Demo</h1>
        <p>Single-page demo for the current FastAPI contract: health, index, and ask.</p>
      </header>

      <section className="card">
        <h2>Health</h2>
        <button type="button" onClick={handleHealthCheck} disabled={healthLoading}>
          {healthLoading ? "Checking..." : "Check API health"}
        </button>
        {healthData ? <p className="status success">Status: {healthData.status}</p> : null}
        {healthError ? <p className="status error">{healthError}</p> : null}
      </section>

      <section className="card">
        <h2>Index Directory</h2>
        <form onSubmit={handleIndexSubmit} className="stack">
          <label>
            Input directory
            <input value={inputDir} onChange={(event) => setInputDir(event.target.value)} required />
          </label>
          <label>
            Index path
            <input value={indexPath} onChange={(event) => setIndexPath(event.target.value)} required />
          </label>
          <button type="submit" disabled={indexLoading}>
            {indexLoading ? "Indexing..." : "Run index"}
          </button>
        </form>
        {indexData ? (
          <div className="result">
            <p className="status success">Indexed {indexData.indexed_chunk_count} chunks.</p>
            <p>Index file: {indexData.index_path}</p>
          </div>
        ) : null}
        {indexError ? (
          <div className="status error">
            <strong>Index request failed.</strong>
            <p>{indexError}</p>
          </div>
        ) : null}
      </section>

      <section className="card">
        <h2>Ask Question</h2>
        <form onSubmit={handleAskSubmit} className="stack">
          <label>
            Query
            <textarea value={query} onChange={(event) => setQuery(event.target.value)} rows={3} required />
          </label>
          <label>
            top_k
            <input
              type="number"
              min={1}
              max={10}
              value={topK}
              onChange={(event) => setTopK(Number(event.target.value))}
              required
            />
          </label>
          <button type="submit" disabled={askLoading}>
            {askLoading ? "Asking..." : "Ask index"}
          </button>
        </form>
        {askData ? (
          <div className="result">
            <h3>Answer</h3>
            <p>{askData.answer}</p>
            <h3>Used context</h3>
            <p>{askData.used_context ? "true" : "false"}</p>
            <h3>Sources</h3>
            {askData.sources.length > 0 ? (
              <ul>
                {askData.sources.map((source) => (
                  <li key={source.chunk_id}>
                    {source.source}
                    {source.page !== null ? ` (page ${source.page})` : ""} - {source.chunk_id}
                  </li>
                ))}
              </ul>
            ) : (
              <p>No sources returned.</p>
            )}
          </div>
        ) : null}
        {askError ? (
          <div className="status error">
            <strong>Ask request failed.</strong>
            <p>{askError}</p>
          </div>
        ) : null}
      </section>
    </main>
  );
}

export default App;
