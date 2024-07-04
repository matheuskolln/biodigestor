import React, { useState } from "react";
import axios from "axios";
import "./Login.css"; // Import your CSS file

const Register = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("https://matheusmedeor.pythonanywhere.com/users", {
        name,
        password,
        email,
      })
      .then((response) => {
        console.log(response.data);
        if (response.data.user) {
          window.location.href = "/";
        }
      })
      .catch((error) => {
        setError("Invalid email or password");
      });
  };

  return (
    <div className="container">
      <div className="login-container">
        <h2 className="login-title">Biodigestor</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nome:</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Senha:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="submit-btn">
            Cadastrar
          </button>
          {error && <p className="error-message">{error}</p>}
        </form>
      </div>
    </div>
  );
};

export default Register;
