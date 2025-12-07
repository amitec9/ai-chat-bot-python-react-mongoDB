import React, { useState, useEffect, useRef } from "react";
import { getMessages, addMessage } from "../api/chat";

const ChatWindow = ({ conversationId, token }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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
    if (!input.trim()) return;
    
    setLoading(true);
    try {
      await addMessage({ conversation_id: conversationId, sender: "user", message: input }, token);
      setInput("");
      fetchMessages();
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-panel">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty">Start a conversation...</div>
        ) : (
          messages.map((msg) => (
            <div key={msg._id} className={`message ${msg.sender}`}>
              <div className="message-content">
                <div className="message-sender">{msg.sender}</div>
                {msg.message}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
