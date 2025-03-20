"use client";
import React from "react";
import Navbar from "../Dashboard/Navbar";


const AboutContainer = () => {
  return (
    <main className="flex flex-col sm:flex-row w-screen bg-neutral-800 h-screen ">
      <div className="flex flex-col items-center">
        <img className="hidden sm:block w-[115px] h-[115px] m-4 mb-10" src="/icons/FlattenedLogo.svg" />
        <Navbar />
      </div>
      <div className="flex flex-1 flex-col items-center sm:order-none order-first">

        <div className="w-[100%]">
          <h1 className="   m-8 text-6xl
                            font-bold text-left 
                            text-white max-w-[866px] 
                            max-md:max-w-[700px] 
                            max-sm:mb-20 
                            max-sm:max-w-full 
                            ">
            About
          </h1>
        </div>

        <div className="flex flex-col w-[134px] sm:w-[100%] h-full items-center justify-center">
          <h1 className="text-center text-2xl font-bold text-white px-40 mb-5">Jammin is a project created for SENG 401 - Software Architecture that uses ChatGPT to parse a user’s Spotify analytics and match them with people with similar music taste. Matches are made based on both user’s top artists, songs and genres, combining to generate a compatibility score between both parties.</h1>
          <br></br>
          <h2 className="text-center text-xl font-bold text-white">Credits: Samiul Haque <br/> Keeryn Johnson <br/> Elias Poitras-Whitecalf <br/> Petr Dubovsky <br/> Ryan Graham <br/> Evan Mann</h2>
        </div>
        
      </div>
      
    </main>
  );
};

export default AboutContainer;
