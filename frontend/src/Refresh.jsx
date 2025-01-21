import React, { useState } from "react";

const backend_url = process.env.REACT_APP_BACKEND_URL;

function Refresh() {
  const [metrics, setMetrics] = useState([]);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent form submission refresh
    try {
      const res = await fetch(backend_url+"/refresh", {
        method: "GET",
      });
      const data = await res.json();
      alert("Latest Prometheus Data Pulled");
      setIsSubmitted(true); // Mark form as submitted
      setMetrics(data.response);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
    return(
        <div className="prometheus_metrics">
            <form  onSubmit={handleSubmit}>
             <button type="submit" className="refresh-button">Refresh Kepler data </button>
            </form>
            <div>
            {/* Conditionally Render Table */}
          {isSubmitted && (
            <table border="1" style={{ width: "100%", textAlign: "left" }}>
                <thead>
                <tr>
                    <th>Time Stamp</th>
                    <th>Node Instance</th>
                    <th>Power Consumption in kWh</th>
                </tr>
                </thead>
                <tbody>
                {metrics.map((metric, index) => (
                    <tr key={index}>
                    <td>{metric.timestamp}</td>
                    <td>{metric.instance}</td>
                    <td>{(metric.value/3600000).toFixed(2)}</td>
                    </tr>
                ))}
                </tbody>
        </table>
        )}
        </div>
        </div>
    );
};

export default Refresh;