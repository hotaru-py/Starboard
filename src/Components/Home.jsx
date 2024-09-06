import gr1 from "../assets/home_graphic.webp";
import Navbar from "./Navbar";

function Home() {
  return (
    <div>
      <main className="bg-[#0D1B2A] text-white min-h-screen">
        <Navbar />
        <div className="container mx-auto flex items-center justify-between min-h-[calc(100vh-96px)]">
          <div className="flex flex-col items-start">
            <h2 className="text-5xl text-left">
              Optimizing Ship Routes <br /> to maximise efficiency and safety
            </h2>
            <h2 className="mt-4 text-2xl font-light text-left">
              Welcome aboard the Starboard!
            </h2>
            <a href="/dashboard">
              <button className="bg-[#415A77] rounded-2xl p-4 text-m mt-8 hover:bg-[#E0E1DD] hover:text-black transition font-bold">
                Dashboard
              </button>
            </a>
          </div>
          <div>
            <img
              src={gr1}
              alt="Graphic"
              className="w-[500px] h-auto hover:scale-125 transition mr-20"
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default Home;
