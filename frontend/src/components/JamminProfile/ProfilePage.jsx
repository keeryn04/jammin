"use client";
import React, { useContext } from "react";
import { UserContext } from "../UserContext"; // Adjust the path as needed
import ProfileContent from "./ProfileContent";
import Sidebar from "../Dashboard/Sidebar";

const ProfilePage = () => {
  const { activeUser } = useContext(UserContext); // Consume the context

  if (!activeUser) {
    return <div>Loading...</div>; // Add a loading state
  }

  function setAppHeight() {
    const vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
    document.documentElement.style.setProperty('--app-height', `${vh}px`);
  }

  window.addEventListener('resize', setAppHeight);
  window.addEventListener('load', setAppHeight);
  setTimeout(setAppHeight, 50); // Small delay to allow UI adjustments

  return (
    <main className="flex flex-col sm:flex-row w-screen bg-neutral-800 h-[var(--app-height)]">
      <Sidebar />
      <ProfileContent activeUser={activeUser} /> {/* Pass activeUser as a prop */}
    </main>
  );
};

export default ProfilePage;