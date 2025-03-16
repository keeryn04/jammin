"use client";
import React, { useRef, useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import SpotifyProfile from "../Profile/SpotifyProfile";
import MusicPlayer from "./MusicPlayer";
import { UserProvider } from "../UserContext"; // Import the provider

export default function MainLayout() {
  const [currentTime, setCurrentTime] = useState(0);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const totalDuration = 260; // 4:20 in seconds
  const profileContainerRef = useRef(null);

  // Handle seek bar interaction
  const handleSeek = (time) => {
    setCurrentTime(time);
    if (profileContainerRef.current) {
      const scrollWidth = profileContainerRef.current.scrollWidth;
      const containerWidth = profileContainerRef.current.clientWidth;
      const scrollPosition = (time / totalDuration) * (scrollWidth - containerWidth);
      profileContainerRef.current.scrollTo({ left: scrollPosition, behavior: "smooth" });
    }
  };

  // Handle scroll events to update currentTime
  useEffect(() => {
    const container = profileContainerRef.current;
    const handleScroll = () => {
      if (container) {
        const scrollWidth = container.scrollWidth;
        const containerWidth = container.clientWidth;
        const scrollPosition = container.scrollLeft;
        const newTime = (scrollPosition / (scrollWidth - containerWidth)) * totalDuration;
        setCurrentTime(newTime);
      }
    };
    if (container) {
      container.addEventListener("scroll", handleScroll);
    }
    return () => {
      if (container) {
        container.removeEventListener("scroll", handleScroll);
      }
    };
  }, [totalDuration]);

  // Toggle dropdown
  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  return (
    <UserProvider>
      <div className="fixed inset-0 flex flex-col text-white bg-neutral-800 overflow-hidden">
        {/* Full-height container */}
        <div className="flex flex-1 overflow-hidden">
          {/* Sidebar */}
          <div className="flex-shrink-0">
            <Sidebar />
          </div>
          {/* Main content area */}
          <main className="flex-1 flex justify-center items-center overflow-hidden">
            {/* Centered content */}
            <div className="flex flex-col items-center gap-2"> {/* Reduced gap to gap-2 */}
              {/* Header with "Jammin'" text and three-dot dropdown */}
              <div className="w-[400px] flex justify-between items-center mb-1"> {/* Adjusted margin-bottom */}
                <h1 className="text-sm font-afacad text-center flex-1">Jammin'</h1>
                <div className="relative">
                  <button onClick={toggleDropdown} className="text-white focus:outline-none">
                    &#8942; {/* Three dots */}
                  </button>
                  {isDropdownOpen && (
                    <div className="absolute right-0 mt-2 w-28 bg-neutral-900 rounded-lg shadow-lg">
                      <ul>
                        <li className="px-4 py-2 hover:bg-red-500 cursor-pointer rounded-md">Remove</li>
                      </ul>
                    </div>
                  )}
                </div>
              </div>

              {/* SpotifyProfile container */}
              <div
                ref={profileContainerRef}
                className="w-[400px] h-[400px] bg-neutral-700 rounded-lg shadow-lg overflow-x-auto overflow-y-hidden"
                style={{ scrollbarWidth: "none", msOverflowStyle: "none" }}
              >
                <SpotifyProfile />
                <style>
                  {`
                    .overflow-x-auto::-webkit-scrollbar {
                      display: none;
                    }
                  `}
                </style>
              </div>

              {/* MusicPlayer */}
              <MusicPlayer
                currentTime={currentTime}
                totalDuration={totalDuration}
                onSeek={handleSeek}
                style={{ width: "400px" }}
              />
            </div>
          </main>
        </div>
      </div>

      {/* Add Afacad font */}
      <style>
        {`
          @font-face {
            font-family: 'Afacad';
            src: url('/path-to-afacad-font.woff2') format('woff2'),
                 url('/path-to-afacad-font.woff') format('woff');
            font-weight: normal;
            font-style: normal;
          }
          .font-afacad {
            font-family: 'Afacad', sans-serif;
          }
        `}
      </style>
    </UserProvider>
  );
}