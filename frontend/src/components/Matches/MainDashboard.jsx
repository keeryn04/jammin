"use client";
import React from "react";
import Sidebar from "../Dashboard/Sidebar";
import MatchesList from "./MatchesList";

const MainDashboard = () => {
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

        <div className="w-[100%]">
          <h1 className="   m-5 text-6xl
                            font-bold text-left 
                            text-white max-w-[866px] 
                            max-md:max-w-[700px] 
                            max-sm:max-w-full 
                            ">
            Matches
          </h1>
        </div>

        <MatchesList />
      </main>
    </div>
  );
};

export default MainDashboard;