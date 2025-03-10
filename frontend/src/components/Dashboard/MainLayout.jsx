"use client";
import React, { useRef, useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import SpotifyProfile from "../Profile/SpotifyProfile";
import MusicPlayer from "./MusicPlayer";

export default function MainLayout() {
  const [currentTime, setCurrentTime] = useState(0);
  const totalDuration = 260; // 4:20 in seconds
  const profileContainerRef = useRef(null);

  const handleSeek = (time) => {
    setCurrentTime(time);
    if (profileContainerRef.current) {
      const scrollWidth = profileContainerRef.current.scrollWidth;
      const containerWidth = profileContainerRef.current.clientWidth;
      const scrollPosition = (time / totalDuration) * (scrollWidth - containerWidth);
      profileContainerRef.current.scrollTo({ left: scrollPosition, behavior: "smooth" });
    }
  };

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

  return (
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
          <div className="flex flex-col items-center gap-10">
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
  );
}
