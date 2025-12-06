import React from "react";

const Navbar = ({ user, handleLogout }) => {
  return (
    <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
      {user ? (
        <>
          <span>Welcome, {user.name}</span>
          <button onClick={handleLogout} style={{ marginLeft: "1rem" }}>
            Logout
          </button>
        </>
      ) : (
        <span>Please login</span>
      )}
    </nav>
  );
};

export default Navbar;
