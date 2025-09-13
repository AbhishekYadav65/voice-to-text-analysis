import React from "react";
import { FaMicrophone } from "react-icons/fa";

const Card = () => {
  return (
    <div className="flex flex-col items-center mt-1 px-4">
      
      {/* Main Heading */}
      <h1 className="text-4xl sm:text-5xl font-bold text-white mb-8 text-center">
        Voice-to-Text Chatbot
      </h1>

      {/* Cards Container */}
      <div className="flex flex-col lg:flex-row justify-center items-start space-y-8 lg:space-y-0 lg:space-x-8 w-full">
        
        {/* Voice Control Card */}
        <div className="w-full sm:max-w-md lg:max-w-sm bg-gray-800 rounded-xl shadow-lg p-6 sm:p-8 flex flex-col items-center space-y-6">
          <h2 className="text-2xl sm:text-3xl font-bold text-white text-center">Voice to Text</h2>
          <FaMicrophone className="text-white text-6xl sm:text-8xl mb-4" />
          <button className="bg-white text-black rounded-xl px-6 sm:px-8 py-3 sm:py-4 text-lg sm:text-xl w-full sm:w-56 hover:bg-gray-300 transition-all duration-300">
            Speak Now
          </button>
          <button className="bg-white text-black rounded-xl px-6 sm:px-8 py-3 sm:py-4 text-lg sm:text-xl w-full sm:w-56 hover:bg-gray-300 transition-all duration-300">
            Stop
          </button>
        </div>

        {/* Transcript Card */}
        <div className="w-full sm:max-w-md lg:max-w-sm bg-gray-900 rounded-xl shadow-lg p-6 sm:p-8 flex flex-col items-center space-y-4">
          <h2 className="text-2xl sm:text-3xl font-bold text-white text-center">Your Transcript</h2>
          <div className="w-full h-64 sm:h-72 bg-gray-700 rounded-lg p-4 overflow-y-auto">
            <p className="text-white text-sm sm:text-base">
              {/* Transcript will appear here */}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Card;
