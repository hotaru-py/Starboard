import { useState } from "react";
import ghlogo from "../assets/github.svg";

function Dashboard() {
  const [slider1Value, setSlider1Value] = useState(50);
  const [slider2Value, setSlider2Value] = useState(50);
  const [slider3Value, setSlider3Value] = useState(50);
  const [slider4Value, setSlider4Value] = useState(50);
  const [slider5Value, setSlider5Value] = useState(50);
  const [slider6Value, setSlider6Value] = useState(50);
  const [slider7Value, setSlider7Value] = useState(50);
  const [slider8Value, setSlider8Value] = useState(50);
  const [fromLocation, setFromLocation] = useState("");
  const [toLocation, setToLocation] = useState("");

  const saveFactors = async () => {
    const data = {
      slider1: slider1Value,
      slider2: slider2Value,
      slider3: slider3Value,
      slider4: slider4Value,
      slider5: slider5Value,
      slider6: slider6Value,
      slider7: slider7Value,
      slider8: slider8Value,
    };

    try {
      const response = await fetch("http://localhost:8000/api/save-factors", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      alert(result.message);
    } catch (error) {
      console.error("Error:", error);
    }
  };

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
      alert(result.message);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <main className="bg-[#0D1B2A] text-white min-h-screen">
        <nav className="bg-[#1B263B]/50 text-white p-6 shadow">
          <div className="container mx-auto flex justify-between items-center">
            <a href="/">
              <div className="flex">
                <h1 className="text-lg font-bold">💫 Starboard</h1>
                <h1 className="ml-1 text-lg font-light">by Team Evergreen</h1>
              </div>
            </a>
            <a
              href="https://github.com/hotaru-hspr/Starboard"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img src={ghlogo} alt="GitHub" className="w-6 h-6" />
            </a>
          </div>
        </nav>

        <div className="container mx-auto py-8 flex items-center justify-between">
          <h2 className="text-5xl font-bold text-left">Welcome Aboard!</h2>

          <div className="flex ml-auto">
            <input
              type="text"
              placeholder="From"
              value={fromLocation}
              onChange={(e) => setFromLocation(e.target.value)}
              className="p-4 w-96 rounded-lg bg-[#E0E1DD] text-black border-2 border-gray-600 focus:outline-none"
              onKeyDown={(e) => e.key === "Enter" && saveLocations()}
            />
            <input
              type="text"
              placeholder="To"
              value={toLocation}
              onChange={(e) => setToLocation(e.target.value)}
              className="p-4 ml-4 w-96 rounded-lg bg-[#E0E1DD] text-black border-2 border-gray-600 focus:outline-none"
              onKeyDown={(e) => e.key === "Enter" && saveLocations()}
            />
          </div>
        </div>

        <div className="flex min-w-screen justify-between px-16 py-4">
          <div
            id="map"
            className="bg-[#415A77] rounded-2xl h-[600px] w-3/5 flex items-center justify-center"
          >
            <div className="text-2xl font-semibold">Map Placeholder</div>
          </div>

          <div className="flex flex-col w-2/5 ml-4">
            <div
              id="config"
              className="bg-[#778DA9] rounded-2xl h-[600px] flex justify-left overflow-y-auto relative"
            >
              <div className="p-8 ">
                <div className="text-3xl font-semibold mb-4 flex sticky items-center top-0 bg-[#778DA9] z-10 pb-4">
                  Configure Feature Weights
                  <button
                    onClick={saveFactors}
                    className="bg-[#415A77] rounded-2xl p-4 text-sm ml-4 hover:bg-[#0D1B2A] transition"
                  >
                    Generate route
                  </button>
                </div>

                {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
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
                        : num === 4
                        ? slider4Value / 100
                        : num === 5
                        ? slider5Value / 100
                        : num === 6
                        ? slider6Value / 100
                        : num === 7
                        ? slider7Value / 100
                        : slider8Value / 100
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
                          : num === 4
                          ? slider4Value
                          : num === 5
                          ? slider5Value
                          : num === 6
                          ? slider6Value
                          : num === 7
                          ? slider7Value
                          : slider8Value
                      }
                      onChange={(e) =>
                        num === 1
                          ? setSlider1Value(e.target.value)
                          : num === 2
                          ? setSlider2Value(e.target.value)
                          : num === 3
                          ? setSlider3Value(e.target.value)
                          : num === 4
                          ? setSlider4Value(e.target.value)
                          : num === 5
                          ? setSlider5Value(e.target.value)
                          : num === 6
                          ? setSlider6Value(e.target.value)
                          : num === 7
                          ? setSlider7Value(e.target.value)
                          : setSlider8Value(e.target.value)
                      }
                      className="w-96 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
