import React, { useEffect, useState } from "react";
import { createConversation, getHistory, deleteConversation } from "../api/chat";
import ConversationList from "../components/ConversationList";
import ChatWindow from "../components/ChatWindow";
import { useNavigate } from "react-router-dom";

const Dashboard = ({ token }) => {
  const navigate = useNavigate();
  const [conversations, setConversations] = useState([]);
  const [selectedConv, setSelectedConv] = useState(null);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!token) {
      navigate("/login");
    } else {
      fetchHistory();
    }
  }, [token, navigate]);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const res = await getHistory(token);
      setConversations(res.data.result || []);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateConversation = async () => {
    if (!title.trim()) return;
    try {
      setLoading(true);
      await createConversation({ title, question: "" }, token);
      setTitle("");
      fetchHistory();
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteConversation = async (id) => {
    try {
      await deleteConversation(id, token);
      if (selectedConv === id) setSelectedConv(null);
      fetchHistory();
    } catch (err) {
      console.log(err);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleCreateConversation();
    }
  };

  return (
    <div className="main-content">
      <div className="sidebar">
        <div className="sidebar-header">
          <h3 className="sidebar-title">Conversations</h3>
          <div className="input-group">
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="New chat title..."
              disabled={loading}
            />
            <button onClick={handleCreateConversation} disabled={loading}>
              {loading ? "..." : "Add"}
            </button>
          </div>
        </div>
        <ConversationList
          conversations={conversations}
          selectConversation={setSelectedConv}
          handleDelete={handleDeleteConversation}
          selectedId={selectedConv}
        />
      </div>
      <div className="chat-panel">
        {selectedConv ? (
          <ChatWindow conversationId={selectedConv} token={token} />
        ) : (
          <div className="chat-empty">Select a conversation to start chatting</div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
