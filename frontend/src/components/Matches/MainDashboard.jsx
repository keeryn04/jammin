"use client";
import React from "react";
import Sidebar from "../Dashboard/Sidebar";
import MatchesList from "./MatchesList";

const MainDashboard = () => {
  return (
    <main className="flex w-full bg-neutral-800 min-h-[screen]">
      <Sidebar />
      <MatchesList />
    </main>
  );
};

export default MainDashboard;
