import { useState } from "react";
import Navbar from "./Navbar";

function Dashboard() {
  const [slider1Value, setSlider1Value] = useState(20);
  const [slider2Value, setSlider2Value] = useState(20);
  const [slider3Value, setSlider3Value] = useState(20);
  const [slider4Value, setSlider4Value] = useState(20);
  const [fromLocation, setFromLocation] = useState("");
  const [toLocation, setToLocation] = useState("");
  const [plotUrl, setPlotUrl] = useState("");

  // const saveFactors = async () => {
  //   const data = {
  //     slider1: slider1Value,
  //     slider2: slider2Value,
  //     slider3: slider3Value,
  //     slider4: slider4Value,
  //   };

  //   try {
  //     const response = await fetch("http://localhost:8000/api/save-factors", {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify(data),
  //     });

  //     const result = await response.json();
  //     alert(result.message);
  //   } catch (error) {
  //     console.error("Error:", error);
  //   }
  // };

  const saveLocations = async () => {
    const data = {
      from_location: fromLocation,
      to_location: toLocation,
    };

    try {
      const response = await fetch("http://localhost:8000/api/save-locations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      console.log(result.from_coords);
      alert(result.message);
      document.getElementById("det").innerHTML =
        "Departing from " +
        fromLocation +
        " (" +
        result.from_coords.lat +
        ", " +
        result.from_coords.lng +
        ")" +
        " - Arriving at " +
        toLocation +
        " (" +
        result.to_coords.lat +
        ", " +
        result.to_coords.lng +
        ")";
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const generatePlot = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/get-ship-route");
      if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setPlotUrl(url); // Set the plot URL in state
      } else {
        console.error("Failed to generate plot");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <main className="bg-[#0D1B2A] text-white min-h-screen">
        <Navbar />

        <div className="container mx-auto py-8 flex items-center justify-between">
          <h2 className="text-5xl font-bold text-left">Dashboard</h2>
          <div className="flex ml-auto">
            <p className="p-4 w-48 bg-transparent font-bold">
              Plan out your journey
            </p>
            <input
              type="text"
              placeholder="Departing from"
              value={fromLocation}
              onChange={(e) => setFromLocation(e.target.value)}
              className="p-4 w-96 rounded-lg bg-[#E0E1DD] text-black border-2 border-gray-600 focus:outline-none"
            />
            <input
              type="text"
              placeholder="Arriving at"
              value={toLocation}
              onChange={(e) => setToLocation(e.target.value)}
              className="p-4 ml-4 w-96 rounded-lg bg-[#E0E1DD] text-black border-2 border-gray-600 focus:outline-none"
            />
            <button
              onClick={() => {
                // saveFactors();
                saveLocations();
                generatePlot();
              }}
              className="bg-[#415A77] rounded-2xl p-4 text-sm ml-4 hover:bg-[#E0E1DD] hover:text-black transition font-bold"
            >
              Generate route
            </button>
          </div>
        </div>

        <div className="flex flex-col">
          <div className="flex min-w-screen justify-between px-16 py-4">
            <div
              id="map"
              className="bg-[#415A77] rounded-2xl h-[500px] w-4/5 flex items-center justify-center"
            >
              <div className="text-2xl font-semibold">
                {plotUrl ? (
                  <img src={plotUrl} alt="Generated Plot" />
                ) : (
                  <p>No route generated yet!</p>
                )}
              </div>
            </div>

            <div className="flex flex-col w-2/5 ml-4">
              <div
                id="config"
                className="bg-[#778DA9] rounded-2xl h-[500px] flex justify-left overflow-y-auto relative"
              >
                <div className="p-8 ">
                  <div className="text-3xl font-semibold mb-4 flex sticky items-center top-0 bg-[#778DA9] z-10 pb-4">
                    Configure Feature Weights
                  </div>

                  {[1, 2, 3, 4].map((num) => (
                    <div className="py-4" key={num}>
                      <label
                        htmlFor={`f${num}`}
                        className="block mb-2 text-xl"
                      >{`Feature ${num}: ${
                        num === 1
                          ? slider1Value / 100
                          : num === 2
                          ? slider2Value / 100
                          : num === 3
                          ? slider3Value / 100
                          : slider4Value / 100
                      }`}</label>
                      <input
                        id={`f${num}`}
                        type="range"
                        value={
                          num === 1
                            ? slider1Value
                            : num === 2
                            ? slider2Value
                            : num === 3
                            ? slider3Value
                            : slider4Value
                        }
                        onChange={(e) =>
                          num === 1
                            ? setSlider1Value(e.target.value)
                            : num === 2
                            ? setSlider2Value(e.target.value)
                            : num === 3
                            ? setSlider3Value(e.target.value)
                            : setSlider4Value(e.target.value)
                        }
                        className="w-96 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="items-center justify-left ml-16 mr-16 mb-16 bg-[#1B263B] rounded-2xl h-[60px] justify-between min-w-screen px-8 py-4 flex">
          <p className="font-bold">Journey Details</p>
          <p id="det" className="ml-12"></p>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
