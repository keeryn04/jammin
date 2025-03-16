"use client";
import React from "react";
import Navbar from "../Dashboard/navbar";
import Heading from "../Generic/Heading";


const SettingsContainer = () => {
  return (
    <main className="flex w-full bg-neutral-700 h-screen ">
      <div className="flex flex-col items-center">
        <img className="w-[115px] h-[115px] m-4 mb-25" src="/icons/FlattenedLogo.svg" />
        <Navbar />
      </div>
      <Heading text="Settings"/>
    </main>
  );
};

export default SettingsContainer;
