import React, { useState, useEffect } from "react";
import { getMessages, addMessage } from "../api/chat";

const ChatWindow = ({ conversationId, token }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    if (conversationId) {
      fetchMessages();
    }
  }, [conversationId]);

  const fetchMessages = async () => {
    try {
      const res = await getMessages(conversationId, token);
      setMessages(res.data.result);
    } catch (err) {
      console.log(err);
    }
  };

  const handleSend = async () => {
    if (!input) return;
    try {
      await addMessage({ conversation_id: conversationId, sender: "user", message: input }, token);
      setInput("");
      fetchMessages();
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div>
      <h3>Chat</h3>
      <div style={{ border: "1px solid #ccc", padding: "1rem", height: "300px", overflowY: "scroll" }}>
        {messages.map((msg) => (
          <div key={msg._id}>
            <strong>{msg.sender}: </strong> {msg.message}
          </div>
        ))}
      </div>
      <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type message" />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default ChatWindow;
