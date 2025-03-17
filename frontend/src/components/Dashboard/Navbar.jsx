import React from "react";
import { useNavigate } from "react-router-dom";

const NavItem = ({ icon, clickFunction }) => (
  <button onClick = {clickFunction} className="group flex justify-center items-center cursor-pointer sm:h-[80%] sm:w-[80%] h-[20%] w-[20%]">
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
    <nav className="flex flex-row items-center bg-neutral-900 w-full h-full
                    sm:flex-col sm:w-[80%] sm:rounded-4xl sm:h-5/7 sm:m-4">
      <div className="flex flex-row sm:flex-col h-full justify-betweem items-center">
        <NavItem icon={"/icons/MatchesIcon.png"} clickFunction={handleMatchesClick} />
        <NavItem icon={"/icons/ProfileIcon.png"} clickFunction={handleProfileClick} />
        <NavItem icon={"/icons/AIIcon.png"} clickFunction={handleAIClick}/>
        <NavItem icon={"/icons/SettingsIcon.png"} clickFunction={handleSettingsClick}/>
        <NavItem icon={"/icons/InfoIcon.png"} clickFunction={handleInfoClick}/>
      </div>
    </nav>
  );
}

