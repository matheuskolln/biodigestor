import React from "react";
import Login from "./Login";
import Measurements from "./Measurements";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/measurements" element={<Measurements />} />
      </Routes>
    </Router>
  );
}

export default App;
