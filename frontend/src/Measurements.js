// Measurements.js

import React, { useState, useEffect } from "react";
import axios from "axios";
import LogoutButton from "./LogoutButton"; // Import your LogoutButton component
import "./Measurements.css"; // Import your CSS file for Measurements

const Measurements = () => {
  const [measurements, setMeasurements] = useState([]);

  useEffect(() => {
    fetchMeasurements();
  }, []);

  const fetchMeasurements = () => {
    axios
      .get("https://matheusmedeor.pythonanywhere.com/measurements")
      .then((response) => {
        console.log(response.data);
        setMeasurements(response.data.measurements);
      })
      .catch((error) => {
        console.error("There was an error fetching the measurements!", error);
      });
  };

  return (
    <div>
      <LogoutButton /> {/* Include the LogoutButton component */}
      <div className="measurements-container">
        <div className="measurements-header">
          <h2 className="measurements-title">Medições</h2>
        </div>
        <table className="measurements-table">
          <thead>
            <tr>
              <th>Temperatura Interna</th>
              <th>Temperatura Externa</th>
              <th>Pressão</th>
              <th>Nível de Gás</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {measurements.map((measurement) => (
              <tr key={measurement.id}>
                <td>{measurement.internal_temperature}°C</td>
                <td>{measurement.external_temperature}°C</td>
                <td>{measurement.main_pressure} hPa</td>
                <td>{measurement.gas_level}%</td>
                <td>{new Date(measurement.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Measurements;
