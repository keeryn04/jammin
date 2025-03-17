"use client";
import React from "react";
import Navbar from "../Dashboard/navbar";
import Heading from "../Generic/Heading";
import ActionButton from "../Generic/ActionButton";


const SettingsContainer = () => {
    const handleLogOut = () => {
      console.log("NOT IMPLEMENTED");
    }

  return (
    <main className="flex flex-col sm:flex-row w-screen bg-neutral-800 h-screen ">
      <div className="flex flex-col items-center">
        <img className="hidden sm:block w-[115px] h-[115px] m-4 mb-25" src="/icons/FlattenedLogo.svg" />
        <Navbar />
      </div>
      <div className="flex flex-1 flex-col items-center sm:order-none order-first">
        <h1 className="   m-8 text-6xl
                          font-bold text-left 
                          text-white max-w-[866px] 
                          max-md:max-w-[700px] 
                          max-sm:mb-20 
                          max-sm:max-w-full 
                          ">
          Settings
        </h1>
        <div className="flex w-[134px] sm:w-[100%] h-full items-center justify-center">
          <ActionButton variant="secondary" onClick={handleLogOut}>Log Out</ActionButton>
        </div>
        
      </div>
      
    </main>
  );
};

export default SettingsContainer;
