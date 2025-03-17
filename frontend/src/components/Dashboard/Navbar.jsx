import React from "react";
import { NavItem, LogOutNavItem } from "./NavItem";
import { useNavigate } from "react-router-dom";

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
  
  const handleInfoClick = () => {
    navigate("/Info");
  }

  const handleLogOutClick = () => {
    
  }
  
  

  return (
    <nav className="flex flex-row items-center bg-neutral-900 w-full h-full
                    sm:flex-col sm:w-[80%] sm:rounded-4xl sm:h-5/7 sm:m-4">
      <div className="flex flex-row sm:flex-col h-full justify-betweem items-center">
        <NavItem icon={"/icons/MatchesIcon.png"} clickFunction={handleMatchesClick} />
        <NavItem icon={"/icons/ProfileIcon.png"} clickFunction={handleProfileClick} />
        <NavItem icon={"/icons/AIIcon.png"} clickFunction={handleAIClick}/>
        <NavItem icon={"/icons/InfoIcon.png"} clickFunction={handleInfoClick}/>
        <LogOutNavItem logout_icon={"/icons/LogOutIcon.png"} red_logout_icon={"/icons/LogOutIconRed.png"} clickFunction={handleLogOutClick}/>
      </div>
    </nav>
  );
}

