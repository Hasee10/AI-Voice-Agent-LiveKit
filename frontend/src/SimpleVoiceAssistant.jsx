import React, { useEffect, useState } from "react";
import {
  useVoiceAssistant,
  BarVisualizer,
  VoiceAssistantControlBar,
  useLocalParticipant,
  useTrackTranscription,
} from "@livekit/components-react";
import { Track } from "livekit-client";
import "./SimpleVoiceAssistant.css";

export function SimpleVoiceAssistant() {
  const { state, audioTrack, agentTranscriptions } = useVoiceAssistant();
  const { localParticipant } = useLocalParticipant();
  const { segments: userTranscriptions } = useTrackTranscription({
    publication: localParticipant?.getTrackPublication(Track.Source.Microphone),
    source: Track.Source.Microphone,
    participant: localParticipant,
  });

  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const allMessages = [
      ...(agentTranscriptions?.map((t) => ({ ...t, type: "agent" })) || []),
      ...(userTranscriptions?.map((t) => ({ ...t, type: "user" })) || []),
    ].sort((a, b) => a.firstReceivedTime - b.firstReceivedTime);
    setMessages(allMessages);
  }, [agentTranscriptions, userTranscriptions]);

  return (
    <div className="voice-assistant-container">
      <div className="chat-log">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <strong>{msg.type === "agent" ? "Agent" : "You"}</strong>
            <p>{msg.text}</p>
          </div>
        ))}
      </div>
      <div className="visualizer-container">
        <BarVisualizer
          state={state}
          barCount={5}
          trackRef={audioTrack}
          className="agent-visualizer"
          options={{ minHeight: 24 }}
        />
      </div>
      <div className="control-section">
        <VoiceAssistantControlBar />
      </div>
    </div>
  );
}