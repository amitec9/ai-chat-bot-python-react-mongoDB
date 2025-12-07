import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = ({ user, handleLogout }) => {
  const navigate = useNavigate();

  const onLogout = () => {
    handleLogout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">💬 AI Chat Bot</div>
      <div className="navbar-user">
        {user ? (
          <>
            <span className="navbar-user-info">Welcome to  <strong>{user.name}    </strong></span>
            <button onClick={onLogout} className="btn-danger">
             Logout
            </button>
          </>
        ) : (
          <div style={{ display: "flex", gap: "1rem" }}>
            {/* <Link to="/login">
              <button>Login</button>
            </Link>
            <Link to="/register">
              <button className="btn-secondary">Register</button>
            </Link> */}
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
