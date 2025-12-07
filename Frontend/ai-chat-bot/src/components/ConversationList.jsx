import React from "react";

const ConversationList = ({ conversations, selectConversation, handleDelete, selectedId }) => {
  return (
    <div className="sidebar-content">
      {conversations.length === 0 ? (
        <div style={{ padding: "1rem", textAlign: "center", color: "var(--text-muted)" }}>
          No conversations yet
        </div>
      ) : (
        conversations.map((conv) => (
          <div
            key={conv._id}
            className={`conversation-item ${selectedId === conv._id ? "active" : ""}`}
            onClick={() => selectConversation(conv._id)}
          >
            <div className="conversation-header">
              <div className="conversation-title">{conv.title}</div>
              <div className="conversation-actions">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(conv._id);
                  }}
                  className="btn-danger"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default ConversationList;
