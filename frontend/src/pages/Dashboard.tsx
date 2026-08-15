import UploadBox from "../components/UploadBox";
import ChatBox from "../components/ChatBox";

export default function Dashboard() {
  return (
    <main className="workspace">
      <section className="panel panel-library" aria-labelledby="library-title">
        <div className="panel-head">
          <h2 id="library-title">Library</h2>
          <p>Upload PDFs to extract knowledge and make them searchable.</p>
        </div>
        <div className="panel-body">
          <UploadBox />
        </div>
      </section>

      <section className="panel panel-chat" aria-labelledby="chat-title">
        <div className="panel-head">
          <h2 id="chat-title">Ask your documents</h2>
          <p>Grounded answers from indexed content in your workspace.</p>
        </div>
        <div className="panel-body">
          <ChatBox />
        </div>
      </section>
    </main>
  );
}
