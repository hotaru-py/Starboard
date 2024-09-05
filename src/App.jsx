import { useState } from "react";
import ghlogo from "./assets/github.svg";

function App() {
  const [slider1Value, setSlider1Value] = useState(50);
  const [slider2Value, setSlider2Value] = useState(50);
  const [slider3Value, setSlider3Value] = useState(50);
  const [slider4Value, setSlider4Value] = useState(50);
  const [slider5Value, setSlider5Value] = useState(50);

  return (
    <div>
      <main className="bg-[#0D1B2A] text-white min-h-screen">
        <nav className="bg-[#1B263B]/50 text-white p-6">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-lg font-semibold">💫 Starboard</h1>
            <a
              href="https://github.com/hotaru-hspr/Starboard-SIH-2024"
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
              className="p-4 w-96 rounded-lg bg-[#E0E1DD] text-black border-2 border-gray-600 focus:outline-none"
            />
            <input
              type="text"
              placeholder="To"
              className="p-4 ml-4 w-96 rounded-lg bg-[#E0E1DD] text-black border-2 border-gray-600 focus:outline-none"
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
              className="bg-[#778DA9] rounded-2xl h-[600px] flex justify-left"
            >
              <div className="p-8">
                <div className="text-3xl font-semibold mb-4">
                  Configure factor weights
                </div>

                {/* Factor slider 1 */}
                <div className="py-4">
                  <label htmlFor="f1" className="block mb-2 text-xl">
                    Factor 1: {slider1Value / 100}
                  </label>
                  <input
                    id="f1"
                    type="range"
                    value={slider1Value}
                    onChange={(e) => setSlider1Value(e.target.value)}
                    className="w-96 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                {/* Factor slider 2 */}
                <div className="py-4">
                  <label htmlFor="f2" className="block mb-2 text-xl">
                    Factor 2: {slider2Value / 100}
                  </label>
                  <input
                    id="f2"
                    type="range"
                    value={slider2Value}
                    onChange={(e) => setSlider2Value(e.target.value)}
                    className="w-96 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                {/* Factor slider 3 */}
                <div className="py-4">
                  <label htmlFor="f3" className="block mb-2 text-xl">
                    Factor 3: {slider3Value / 100}
                  </label>
                  <input
                    id="f3"
                    type="range"
                    value={slider3Value}
                    onChange={(e) => setSlider3Value(e.target.value)}
                    className="w-96 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                {/* Factor slider 4 */}
                <div className="py-4">
                  <label htmlFor="f4" className="block mb-2 text-xl">
                    Factor 4: {slider4Value / 100}
                  </label>
                  <input
                    id="f4"
                    type="range"
                    value={slider4Value}
                    onChange={(e) => setSlider4Value(e.target.value)}
                    className="w-96 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>

                {/* Factor slider 5 */}
                <div className="py-4">
                  <label htmlFor="f5" className="block mb-2 text-xl">
                    Factor 5: {slider5Value / 100}
                  </label>
                  <input
                    id="f5"
                    type="range"
                    value={slider5Value}
                    onChange={(e) => setSlider5Value(e.target.value)}
                    className="w-96 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
