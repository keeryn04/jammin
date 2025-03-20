import React from "react";
import { NavItem, LogOutNavItem } from "./NavItem";
import { useNavigate } from "react-router-dom";

const VERCEL_URL = import.meta.env.VITE_VERCEL_URL_PREVIEW;
const logoutLink = `${VERCEL_URL}/api/logout`;

export default function Navbar() {
  const navigate = useNavigate()

  const handleMatchesClick = () => {
    navigate("/Matches");
  }
  
  const handleProfileClick = () => {
    navigate("/PublicProfile");
  }
  
  const handleAIClick = () => {
    navigate("/Matching");
  }
  
  const handleInfoClick = () => {
    navigate("/About");
  }

  const handleLogOutClick = () => {
    try {
      window.location.href = logoutLink; 
    } catch (e) {
      console.error("Error:", e);
      setError("Error logging out, please try again.");
    }
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

