import React from "react";
import "./LogoutButton.css";

const LogoutButton = () => {
  const handleLogout = () => {
    window.location.href = "/";
  };

  return (
    <button onClick={handleLogout} className="logout-btn">
      Logout
    </button>
  );
};

export default LogoutButton;
