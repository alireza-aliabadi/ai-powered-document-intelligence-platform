import { useState, type FormEvent, type KeyboardEvent } from "react";
import { askQuestion } from "../api/chat";

type Turn = {
  role: "user" | "assistant";
  text: string;
};

export default function ChatBox() {
  const [question, setQuestion] = useState("");
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);

  async function send() {
    const trimmed = question.trim();
    if (!trimmed || busy) return;

    setBusy(true);
    setQuestion("");
    setTurns((prev) => [...prev, { role: "user", text: trimmed }]);

    try {
      const result = await askQuestion(trimmed);
      setTurns((prev) => [
        ...prev,
        { role: "assistant", text: result.answer || "No answer returned." },
      ]);
    } catch (err: unknown) {
      const axiosErr = err as {
        response?: { data?: { answer?: string; error?: string } };
        message?: string;
      };
      const detail =
        axiosErr.response?.data?.answer ||
        axiosErr.response?.data?.error ||
        axiosErr.message ||
        "Could not reach the chat API. Confirm the backend is running and your model key is set.";
      setTurns((prev) => [...prev, { role: "assistant", text: detail }]);
    } finally {
      setBusy(false);
    }
  }

  function onSubmit(event: FormEvent) {
    event.preventDefault();
    void send();
  }

  function onKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void send();
    }
  }

  return (
    <>
      <div className="chat-thread" aria-live="polite">
        {turns.length === 0 ? (
          <div className="chat-empty">
            <strong>Start a conversation</strong>
            Ask about policies, summaries, or facts inside your uploaded documents.
          </div>
        ) : (
          turns.map((turn, index) => (
            <div
              key={`${turn.role}-${index}`}
              className={`bubble ${turn.role === "user" ? "bubble-user" : "bubble-assistant"}`}
            >
              <span className="bubble-label">{turn.role === "user" ? "You" : "DocuMind"}</span>
              {turn.text}
            </div>
          ))
        )}
      </div>

      <form className="composer" onSubmit={onSubmit}>
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Ask a question about your documents…"
          rows={2}
          disabled={busy}
        />
        <button type="submit" className="btn btn-primary" disabled={busy || !question.trim()}>
          {busy ? "Thinking…" : "Ask"}
        </button>
      </form>
    </>
  );
}
