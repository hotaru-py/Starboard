import ghlogo from "../assets/github.svg";

function Home() {
  return (
    <div>
      <main className="bg-[#1B263B] text-white min-h-screen">
        <nav className="bg-transparent text-white p-6 shadow">
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

        <div className="container mx-auto flex flex-col items-start justify-center min-h-[calc(100vh-96px)]">
          <h2 className="text-5xl font-bold text-left">
            Welcome aboard
            <span className="block pb-4"></span>
            the Starboard!
          </h2>
          <a href="/dashboard">
            <button className="bg-[#415A77] rounded-2xl p-4 text-sm mt-8 hover:bg-[#0D1B2A] transition font-bold">
              Dashboard
            </button>
          </a>
        </div>
      </main>
    </div>
  );
}

export default Home;
