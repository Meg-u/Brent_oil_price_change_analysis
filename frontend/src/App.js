import React, { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

function App() {
  const [impactData, setImpactData] = useState([]);
  const [priceData, setPriceData] = useState([]);

  useEffect(() => {
    // Fetch change point impact data
    axios.get("http://127.0.0.1:5000/api/impact")
      .then(res => setImpactData(res.data))
      .catch(err => console.error(err));

    // Fetch historical price data
    axios.get("http://127.0.0.1:5000/api/prices")
      .then(res => setPriceData(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Brent Oil Price Change Point Dashboard</h1>

      {/* Impact Summary Table */}
      <h2>Change Point Impact Summary</h2>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", marginBottom: "30px" }}>
        <thead>
          <tr>
            <th>Change Point Date</th>
            <th>Mean Price Before</th>
            <th>Mean Price After</th>
            <th>% Change in Mean Price</th>
            <th>Volatility Before</th>
            <th>Volatility After</th>
          </tr>
        </thead>
        <tbody>
          {impactData.map((row, index) => (
            <tr key={index}>
              <td>{row["Change Point Date"]}</td>
              <td>{row["Mean Price Before"].toFixed(2)}</td>
              <td>{row["Mean Price After"].toFixed(2)}</td>
              <td>{row["Percent Change in Mean Price"].toFixed(2)}%</td>
              <td>{row["Volatility Before"].toFixed(2)}</td>
              <td>{row["Volatility After"].toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Price Chart */}
      <h2>Brent Oil Price Over Time</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={priceData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Price" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default App;
