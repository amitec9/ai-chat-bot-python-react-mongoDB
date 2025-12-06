import React from "react";

const ConversationList = ({ conversations, selectConversation, handleDelete, selectedId }) => {
  return (
    <div>
      <h3>Chat History</h3>
      {conversations.map((conv) => (
        <div
          key={conv._id}
          style={{ margin: "0.5rem 0", padding: "0.5rem", border: selectedId === conv._id ? "2px solid blue" : "1px solid gray" }}
        >
          <strong>{conv.title}</strong>
          <button onClick={() => handleDelete(conv._id)} style={{ marginLeft: "1rem" }}>Delete</button>
          <button onClick={() => selectConversation(conv._id)} style={{ marginLeft: "0.5rem" }}>Open</button>
        </div>
      ))}
    </div>
  );
};

export default ConversationList;
