import { useState } from "react";
import { LiveKitModal } from "./LiveKitModal";
import "./App.css";

function App() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="app-container">
      <h1>AutoZone Service</h1>
      <p>Your AI-powered car service assistant</p>
      <button onClick={() => setShowModal(true)}>
        <span>Talk to Agent</span>
      </button>
      {showModal && <LiveKitModal setShowModal={setShowModal} />}
    </div>
  );
}

export default App;