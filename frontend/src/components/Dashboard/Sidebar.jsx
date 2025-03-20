import React from "react";
import Navbar from "./Navbar";

export default function Sidebar() {
  return (  
  <div className="flex flex-col items-center">
    <img className="hidden sm:block w-[115px] h-[115px] m-4 mb-10" src="/icons/FlattenedLogo.svg" />
    <Navbar />
  </div>
  );
}

