import React from "react";
import { useNavigate } from "react-router-dom";

const NavItem = ({ icon, clickFunction }) => (
  <button onClick = {clickFunction} className="group flex justify-center items-center cursor-pointer lg:h-[100%] lg:w-[100%] md:h-[90%] md:w-[90%] sm:h-[80%] sm:w-[80%] ">
    <img className="hover:brightness-200" src={`${icon}`} />
  </button>
);

export default function Navbar() {
  const navigate = useNavigate()

  const handleMatchesClick = () => {
    navigate("/Matching");
  }
  
  const handleProfileClick = () => {
    navigate("/PublicProfile");
  }
  
  const handleAIClick = () => {
    navigate("/Matching");
  }
  
  const handleSettingsClick = () => {
    navigate("/Settings");
  }
  
  const handleInfoClick = () => {
    navigate("/Info");
  }

  return (
    <nav className="flex flex-col lg:w-[80%] md:w-[70%] sm:w-[60%] items-center bg-neutral-800 rounded-full h-2/3 m-4">
      <div className="flex flex-col flex-1 justify-evenly items-center">
        <NavItem icon={"/icons/MatchesIcon.png"} clickFunction={handleMatchesClick} />
        <NavItem icon={"/icons/ProfileIcon.png"} clickFunction={handleProfileClick} />
        <NavItem icon={"/icons/AIIcon.png"} clickFunction={handleAIClick}/>
        <NavItem icon={"/icons/SettingsIcon.png"} clickFunction={handleSettingsClick}/>
        <NavItem icon={"/icons/InfoIcon.png"} clickFunction={handleInfoClick}/>
      </div>
    </nav>
  );
}

