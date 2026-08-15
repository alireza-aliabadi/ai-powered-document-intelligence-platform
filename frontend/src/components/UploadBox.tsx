import { useRef, useState, type DragEvent } from "react";
import { FileText, UploadCloud } from "lucide-react";
import { getJobStatus, uploadDocument } from "../api/documents";

function formatBytes(size: number) {
  if (size < 1024) return `${size} B`;
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
  return `${(size / (1024 * 1024)).toFixed(1)} MB`;
}

async function waitForJob(taskId: string, timeoutMs = 180_000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    const job = await getJobStatus(taskId);
    if (job.done) {
      if (job.status === "SUCCESS") return;
      throw new Error(job.error || "Processing failed");
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
  throw new Error("Processing timed out");
}

export default function UploadBox() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [dragging, setDragging] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);

  function pickFile(next?: File | null) {
    setFile(next ?? null);
    setMessage("");
    setError(false);
  }

  function onDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setDragging(false);
    const next = event.dataTransfer.files?.[0];
    if (next) pickFile(next);
  }

  async function upload() {
    if (!file || busy) return;
    setBusy(true);
    setError(false);
    setMessage("Uploading…");
    try {
      const { task_id } = await uploadDocument(file);
      setMessage("Uploading…");
      await waitForJob(task_id);
      setMessage("Done");
    } catch (err) {
      setError(true);
      setMessage(err instanceof Error ? err.message : "Upload failed. Check the API and try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <div
        className={`dropzone${dragging ? " is-dragging" : ""}`}
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
      >
        <div className="dropzone-icon" aria-hidden="true">
          <UploadCloud size={22} strokeWidth={1.8} />
        </div>
        <h3>Drop a document here</h3>
        <p>PDF preferred · click to browse</p>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={(event) => pickFile(event.target.files?.[0] ?? null)}
        />
      </div>

      {file ? (
        <div className="file-chip">
          <FileText size={18} color="#4ec9b4" aria-hidden="true" />
          <div style={{ minWidth: 0, flex: 1 }}>
            <strong>{file.name}</strong>
            <span>{formatBytes(file.size)}</span>
          </div>
          <button type="button" className="btn btn-ghost" onClick={() => pickFile(null)}>
            Clear
          </button>
        </div>
      ) : null}

      <button type="button" className="btn btn-primary" disabled={!file || busy} onClick={upload}>
        {busy ? "Uploading…" : "Upload to workspace"}
      </button>

      {message ? (
        <p className={`status-line${error ? " is-error" : " is-ok"}`}>{message}</p>
      ) : null}
    </>
  );
}
