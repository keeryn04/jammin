import React from "react";
import Logo from "./Logo"; // Import the Logo component
import TurntableArm from "./turntable-png-17.png"; // Import the image

const Loading = () => {
  return (
    <div className="relative flex justify-center items-center h-screen overflow-visible">
      {/* Spinning Record (Logo) */}
      <div className="w-[407px] h-[407px] flex justify-center items-center animate-spin">
        <Logo />
      </div>

      {/* Static Record Player Arm */}
      <img
        src={TurntableArm} // Use the imported image
        alt="Record Player Arm"
        className="absolute top-[48%] left-[69%] transform -translate-x-1/2 -translate-y-1/2 w-20 h-20 pointer-events-none z-10"
        />

      {/* Optional Loading Text */}
      <p className="absolute bottom-10 text-white text-lg">Jammin' Away...</p>
      <p className="absolute bottom-5 text-gray-500 text-sm">{'(LLM Processing Data)'}</p>
    </div>
  );
};

export default Loading;