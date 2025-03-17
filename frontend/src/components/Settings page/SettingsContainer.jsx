"use client";
import React from "react";
import Navbar from "../Dashboard/navbar";
import Heading from "../Generic/Heading";


const SettingsContainer = () => {
  return (
    <main className="flex flex-col sm:flex-row w-screen bg-neutral-700 h-screen ">
      <div className="flex flex-col items-center">
        <img className="hidden sm:block w-[115px] h-[115px] m-4 mb-25" src="/icons/FlattenedLogo.svg" />
        <Navbar />
      </div>
      <div className="flex flex-1 flex-col sm:order-none order-first">
        <Heading text="Settings"/>
      </div>
      
    </main>
  );
};

export default SettingsContainer;
