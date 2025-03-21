"use client";
import React from "react";
import Sidebar from "../Dashboard/Sidebar";
import MatchesList from "./MatchesList";

const MainDashboard = () => {
  function setAppHeight() {
    const vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
    document.documentElement.style.setProperty('--app-height', `${vh}px`);
  }

  window.addEventListener('resize', setAppHeight);
  window.addEventListener('load', setAppHeight);
  setTimeout(setAppHeight, 50); // Small delay to allow UI adjustments

  return (
    <div className="flex flex-col sm:flex-row w-screen bg-neutral-800 h-[var(--app-height)]">
      <Sidebar />

      {/* Main content area */}
      <main className="flex flex-1 flex-col flex-grow items-center sm:order-none order-first
      overflow-y-auto [&::-webkit-scrollbar]:w-2
      [&::-webkit-scrollbar-track]:rounded-full
      [&::-webkit-scrollbar-track]:bg-gray-100
      [&::-webkit-scrollbar-thumb]:rounded-full
      [&::-webkit-scrollbar-thumb]:bg-gray-300
      dark:[&::-webkit-scrollbar-track]:bg-neutral-700
      dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500">
        <MatchesList />
      </main>
    </div>
  );
};

export default MainDashboard;