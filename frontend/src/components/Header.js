import React from "react";

const Header = () => {
  return (
    <div className="w-full bg-[#000000] relative overflow-hidden">
      {/* Grid Background */}
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: `
            linear-gradient(to right, #e2e8f0 1px, transparent 1px),
            linear-gradient(to bottom, #e2e8f0 1px, transparent 1px)
          `,
          backgroundSize: "20px 30px",
          WebkitMaskImage:
            "radial-gradient(ellipse 70% 60% at 50% 0%, #000 60%, transparent 100%)",
          maskImage:
            "radial-gradient(ellipse 70% 60% at 50% 0%, #000 60%, transparent 100%)",
        }}
      />

      {/* Foreground Content */}
      <div className="relative z-10 flex flex-col items-center justify-center text-center px-4 py-16 sm:py-20 md:py-24">
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl text-white font-bold">
          Transform Your Voice
        </h1>
        <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl text-white font-bold mt-4 sm:mt-6">
          Into Seamless Conversations
        </h2>
        <p className="text-sm sm:text-base md:text-lg lg:text-xl text-white mt-4 sm:mt-6 max-w-xs sm:max-w-md md:max-w-lg lg:max-w-2xl">
          Speak naturally and watch your words turn into text instantly.
        </p>
        <button className="bg-white text-black rounded-xl mt-6 sm:mt-8 px-6 sm:px-8 py-3 sm:py-4 text-base sm:text-lg md:text-xl w-40 sm:w-48 md:w-56 h-12 sm:h-14 md:h-16 hover:bg-gray-300 transition-all duration-300">
          Start Now
        </button>
      </div>
    </div>
  );
};

export default Header;
