"use client";
import React, { useRef, useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import SpotifyProfile from "../Profile/SpotifyProfile"; // Import the full profile
import MusicPlayer from "./MusicPlayer";

export default function MainLayout() {
  const [currentTime, setCurrentTime] = useState(0);
  const totalDuration = 260; // 4:20 in seconds
  const profileContainerRef = useRef(null); // Ref for the SpotifyProfile container

  // Function to handle seeking in the MusicPlayer
  const handleSeek = (time) => {
    setCurrentTime(time);

    // Calculate the scroll position based on the currentTime
    if (profileContainerRef.current) {
      const scrollWidth = profileContainerRef.current.scrollWidth;
      const containerWidth = profileContainerRef.current.clientWidth;
      const scrollPosition = (time / totalDuration) * (scrollWidth - containerWidth);
      profileContainerRef.current.scrollTo({ left: scrollPosition, behavior: "smooth" });
    }
  };

  // Handle scroll events on the SpotifyProfile container
  useEffect(() => {
    const container = profileContainerRef.current;

    const handleScroll = () => {
      if (container) {
        const scrollWidth = container.scrollWidth;
        const containerWidth = container.clientWidth;
        const scrollPosition = container.scrollLeft;
        const newTime = (scrollPosition / (scrollWidth - containerWidth)) * totalDuration;
        setCurrentTime(newTime); // Update the currentTime state
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
    <>
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css"
      />
      <link
        href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700&family=Afacad:wght@400;500;600;700&display=swap"
        rel="stylesheet"
      />
      <div className="flex min-h-screen text-white bg-neutral-800">
        <Sidebar />
        <main className="flex-1 p-5 max-md:p-4 max-sm:p-2.5">
          {/* Square Box Container with Horizontal Scroll */}
          <div
            ref={profileContainerRef}
            className="w-[400px] h-[400px] bg-neutral-700 rounded-lg shadow-lg overflow-x-auto overflow-y-hidden"
            style={{
              scrollbarWidth: "none", // Firefox
              msOverflowStyle: "none", // IE and Edge
            }}
          >
            <SpotifyProfile /> {/* Full profile component */}
            <style>
              {`
                .overflow-x-auto::-webkit-scrollbar {
                  display: none; /* Chrome, Safari, and Opera */
                }
              `}
            </style>
          </div>
          <MusicPlayer currentTime={currentTime} totalDuration={totalDuration} onSeek={handleSeek} />
        </main>
      </div>
    </>
  );
}