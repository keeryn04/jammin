"use client";
import React from "react";
import Sidebar from "../Dashboard/Sidebar";
import MatchesList from "./MatchesList";

const MainDashboard = () => {
  return (
    <div className="fixed inset-0 flex flex-col text-white bg-neutral-800 overflow-hidden">
      {/* Full-height container */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <div className="flex-shrink-0">
          <Sidebar />
        </div>
        {/* Main content area */}
        <main className="flex-1 overflow-y-auto">
          <MatchesList />
        </main>
      </div>
    </div>
  );
};

export default MainDashboard;