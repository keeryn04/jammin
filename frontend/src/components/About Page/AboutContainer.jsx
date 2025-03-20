"use client";
import React from "react";
import Navbar from "../Dashboard/Navbar";
import Sidebar from "../Dashboard/Sidebar";


const AboutContainer = () => {

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
      <Sidebar/>  
      <div className="flex flex-1 flex-col flex-grow items-center sm:order-none order-first">

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

        <div className="flex flex-col w-[80%] sm:w-[100%] h-full items-center justify-center">
          <h1 className="text-center text-md sm:text-2xl font-bold text-white sm:px-40 mb-5">Jammin is a project created for SENG 401 - Software Architecture that uses ChatGPT to parse a user’s Spotify analytics and match them with people with similar music taste. Matches are made based on both user’s top artists, songs and genres, combining to generate a compatibility score between both parties.</h1>
          <br></br>
          <h2 className="text-center text-sm sm:text-xl font-bold text-white">Credits: Samiul Haque <br/> Keeryn Johnson <br/> Elias Poitras-Whitecalf <br/> Petr Dubovsky <br/> Ryan Graham <br/> Evan Mann</h2>
        </div>
        
      </div>
      
    </main>
  );
};

export default AboutContainer;
