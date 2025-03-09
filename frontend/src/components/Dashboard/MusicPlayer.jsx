"use client";
import React, { useState, useRef, useEffect } from "react";
import { PrevButton, PlayButton, NextButton, RedPlayButton } from "./icons"; // Import RedPlayButton

export default function MusicPlayer({ currentTime, totalDuration, onSeek, style }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isHoveringPlayButton, setIsHoveringPlayButton] = useState(false); // State to track hover
  const seekBarRef = useRef(null); // Ref for the seek bar container

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  // Handle seek bar interaction (click)
  const handleSeek = (e) => {
    const rect = seekBarRef.current.getBoundingClientRect();
    const offsetX = e.clientX - rect.left;
    const percentage = offsetX / rect.width;
    const newTime = percentage * totalDuration;
    onSeek(newTime); // Update the scroll position
  };

  // Handle drag start
  const handleDragStart = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  // Handle dragging
  const handleDragging = (e) => {
    if (isDragging) {
      const rect = seekBarRef.current.getBoundingClientRect();
      const offsetX = e.clientX - rect.left;
      const percentage = Math.min(Math.max(offsetX / rect.width, 0), 1); // Clamp between 0 and 1
      const newTime = percentage * totalDuration;
      onSeek(newTime); // Update the scroll position
    }
  };

  // Handle drag end
  const handleDragEnd = () => {
    setIsDragging(false);
  };

  // Add event listeners for dragging
  useEffect(() => {
    const handleMouseMove = (e) => handleDragging(e);
    const handleMouseUp = () => handleDragEnd();

    if (isDragging) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    }

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isDragging]);

  return (
    <section className="mt-10 text-center" style={style}> {/* Apply the style prop here */}
      <h2 className="mb-2 text-2xl font-semibold">A Display Caption?</h2>
      <p className="mb-4 text-base text-zinc-400">Person's Name</p>
      <div className="mx-auto mt-0 mb-5 w-full"> {/* Removed max-w-[400px] */}
        <div
          ref={seekBarRef}
          className="relative mb-2 w-full h-1 rounded-sm bg-neutral-500 cursor-pointer"
          onClick={handleSeek}
        >
          <div
            className="w-1.5 h-full bg-white rounded-sm"
            style={{ width: `${(currentTime / totalDuration) * 100}%` }}
          />
          <div
            className="absolute left-0 top-2/4 -translate-y-2/4 h-[13px] w-[13px] cursor-grab"
            style={{ left: `${(currentTime / totalDuration) * 100}%` }}
            onMouseDown={handleDragStart}
            aria-label="Seek"
          >
            <div className="w-full h-full bg-white rounded-full" />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[4px] h-[4px] bg-neutral-500 rounded-full" />
          </div>
        </div>
        <div className="flex justify-between text-xs text-zinc-400">
          <span>{formatTime(currentTime)}</span>
          <span>-{formatTime(totalDuration - currentTime)}</span>
        </div>
      </div>
      <div className="flex gap-11 justify-center items-center max-sm:gap-8">
        {/* Previous Track Icon (as button) */}
        <div
          className="cursor-pointer focus:outline-none hover:scale-90 transition-transform duration-200"
          aria-label="Previous track"
        >
          <PrevButton className="w-8 h-8" /> {/* Adjust size as needed */}
        </div>

        {/* Play/Pause Icon (as button) */}
        <div
          className="cursor-pointer focus:outline-none relative"
          aria-label="Play"
          onMouseEnter={() => setIsHoveringPlayButton(true)} // Set hover state to true
          onMouseLeave={() => setIsHoveringPlayButton(false)} // Set hover state to false
        >
          {/* Red circle behind the Play icon */}
          <div className="absolute inset-0 flex items-center justify-center z-0">
            <div className="w-8 h-8 bg-red-500 rounded-full opacity-0 hover:opacity-100 transition-opacity duration-200" />
          </div>
          {/* Play icon */}
          <div className="relative z-10">
            {isHoveringPlayButton ? (
              <RedPlayButton className="w-10 h-10" /> // Smaller size for RedPlayButton
            ) : (
              <PlayButton className="w-12 h-12" /> // Default size for PlayButton
            )}
          </div>
        </div>

        {/* Next Track Icon (as button) */}
        <div
          className="cursor-pointer focus:outline-none hover:scale-90 transition-transform duration-200"
          aria-label="Next track"
        >
          <NextButton className="w-8 h-8" /> {/* Adjust size as needed */}
        </div>
      </div>
    </section>
  );
}