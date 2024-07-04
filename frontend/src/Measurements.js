import React, { useState, useEffect } from "react";
import axios from "axios";
import LogoutButton from "./LogoutButton";
import "./Measurements.css";

const Measurements = () => {
  const [measurements, setMeasurements] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

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

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = measurements.slice(indexOfFirstItem, indexOfLastItem);

  const pageNumbers = [];
  for (let i = 1; i <= Math.ceil(measurements.length / itemsPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <div className="measurements-container">
      <LogoutButton className="logout-button" />
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
          {currentItems.map((measurement) => (
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
      <div className="pagination">
        {pageNumbers.map((number) => (
          <button
            key={number}
            onClick={() => handlePageChange(number)}
            className={`page-item ${currentPage === number ? "active" : ""}`}
          >
            {number}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Measurements;
