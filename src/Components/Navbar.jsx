import ghlogo from "../assets/github.svg";

function Navbar() {
  return (
    <nav className="bg-[#0D1B2A] text-white p-6 shadow sticky top-0">
      <div className="container mx-auto flex justify-between items-center">
        <a href="/">
          <div className="flex hover:text-blue-300 transition">
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
  );
}

export default Navbar;
