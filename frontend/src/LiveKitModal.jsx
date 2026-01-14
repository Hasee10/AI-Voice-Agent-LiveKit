import { LiveKitRoom, RoomAudioRenderer } from "@livekit/components-react";
import "@livekit/components-styles";
import { SimpleVoiceAssistant } from "./SimpleVoiceAssistant";

export function LiveKitModal({ setShowModal }) {
  const serverUrl = import.meta.env.VITE_LIVEKIT_URL;
  
  // PASTE YOUR TOKEN BELOW (See Step 5 instructions)
  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Njg0NzI1MTQsImlkZW50aXR5IjoicGFydGljaXBhbnQtNjIyZmM2MTIyZmU2IiwiaXNzIjoiQVBJVGQySnJ0ZWF3Sk16IiwibmFtZSI6InBhcnRpY2lwYW50LTYyMmZjNjEyMmZlNiIsIm5iZiI6MTc2ODM4NjExNCwic3ViIjoicGFydGljaXBhbnQtNjIyZmM2MTIyZmU2IiwidmlkZW8iOnsicm9vbSI6Im15LXRlc3Qtcm9vbSIsInJvb21Kb2luIjp0cnVlfX0.0FkIBBA3bkdaq9E5jW-0lCv6nEm_xqwNPXJ4MUGDDSw";

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-btn" onClick={() => setShowModal(false)}>X</button>
        <LiveKitRoom
          video={false}
          audio={true}
          token={token}
          serverUrl={serverUrl}
          connect={true}
          onDisconnected={() => setShowModal(false)}
        >
          <SimpleVoiceAssistant />
          <RoomAudioRenderer />
        </LiveKitRoom>
      </div>
    </div>
  );
}