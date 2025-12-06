import React, { useEffect, useState } from "react";
import { createConversation, getHistory, deleteConversation } from "../api/chat";
import ConversationList from "../components/ConversationList";
import ChatWindow from "../components/ChatWindow";

const Dashboard = ({ token }) => {
  const [conversations, setConversations] = useState([]);
  const [selectedConv, setSelectedConv] = useState(null);
  const [title, setTitle] = useState("");

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await getHistory(token);
      setConversations(res.data.result);
    } catch (err) {
      console.log(err);
    }
  };

  const handleCreateConversation = async () => {
    if (!title) return;
    try {
      await createConversation({ title, question: "" }, token);
      setTitle("");
      fetchHistory();
    } catch (err) {
      console.log(err);
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

  return (
    <div style={{ display: "flex", gap: "2rem" }}>
      <div>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Chat Title" />
        <button onClick={handleCreateConversation}>Create</button>
        <ConversationList
          conversations={conversations}
          selectConversation={setSelectedConv}
          handleDelete={handleDeleteConversation}
          selectedId={selectedConv}
        />
      </div>
      <div style={{ flex: 1 }}>
        {selectedConv && <ChatWindow conversationId={selectedConv} token={token} />}
      </div>
    </div>
  );
};

export default Dashboard;
