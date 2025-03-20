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
    <main className="flex flex-col sm:flex-row w-screen bg-neutral-800 h-[var(--app-height)]
      overflow-y-auto [&::-webkit-scrollbar]:w-2
      [&::-webkit-scrollbar-track]:rounded-full
      [&::-webkit-scrollbar-track]:bg-gray-100
      [&::-webkit-scrollbar-thumb]:rounded-full
      [&::-webkit-scrollbar-thumb]:bg-gray-300
      dark:[&::-webkit-scrollbar-track]:bg-neutral-700
      dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500">
      <Sidebar />
      <ProfileContent activeUser={activeUser} /> {/* Pass activeUser as a prop */}
    </main>
  );
};

export default ProfilePage;