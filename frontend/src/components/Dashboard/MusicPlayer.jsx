"use client";
import React, { useState, useRef, useEffect, useContext } from "react";
import { UserContext } from "../UserContext"; // Import the context
import { PrevButton, PlayButton, NextButton, RedPlayButton } from "./icons"; // Import icons

export default function MusicPlayer({
  currentTime,
  totalDuration,
  onSeek,
  style,
  showHeart,
  setShowHeart,
  randomEmoji,
  setRandomEmoji,
}) {
  const {
    activeUser,
    displayedUsers,
    setDisplayedUsers,
    currentDisplayedUser,
    setCurrentDisplayedUser,
    currentIndex,
    setCurrentIndex,
  } = useContext(UserContext);

  const [isDragging, setIsDragging] = useState(false);
  const [isHoveringPlayButton, setIsHoveringPlayButton] = useState(false);
  const seekBarRef = useRef(null);

  // Array of emojis to choose from
  const emojis = ["😍", "❤️", "🔥", "💖", "🥰", "😘", "💕"];

  // Function to get a random emoji
  const getRandomEmoji = () => {
    const randomIndex = Math.floor(Math.random() * emojis.length);
    return emojis[randomIndex];
  };

  // Format time helper
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
    onSeek(newTime);
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
      onSeek(newTime);
    }
  };

  // Handle drag end
  const handleDragEnd = () => {
    setIsDragging(false);
  };

  const handleNextUser = () => {
    setCurrentIndex((prevIndex) => {
      const allUsers = [...displayedUsers];
      let nextIndex = (prevIndex + 1) % allUsers.length; // Calculate next index
      setCurrentDisplayedUser(allUsers[nextIndex]); // Update currentDisplayedUser
      console.log(activeUser);
      return nextIndex; // Return the new index
    });
  };

  const handlePreviousUser = () => {
    setCurrentIndex((prevIndex) => {
      const allUsers = [...displayedUsers];
      let previousIndex = (prevIndex - 1 + allUsers.length) % allUsers.length; // Calculate previous index
      setCurrentDisplayedUser(allUsers[previousIndex]); // Update currentDisplayedUser
      console.log(activeUser);
      return previousIndex; // Return the new index
    });
  };

  const handlePlay = async () => {
    if (!activeUser || !currentDisplayedUser) return;

    try {
      // Fetch all matches from the backend
      const matchesResponse = await fetch("http://localhost:5001/api/matches");
      const matchesData = await matchesResponse.json();

      // Find the match where user_1_id matches activeUser.user_data_id and user_2_id matches currentDisplayedUser.user_data_id
      const match = matchesData.find(
        (match) =>
          match.user_1_id === activeUser.user_data_id &&
          match.user_2_id === currentDisplayedUser.user_data_id
      );

      // If no match is found, log an error and return
      if (!match) {
        console.error("Match not found!");
        return;
      }

      // Update the match status to 'waiting'
      const updateResponse = await fetch(
        `http://localhost:5001/api/matches/${match.match_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_1_id: match.user_1_id,
            user_2_id: match.user_2_id,
            match_score: match.match_score, // Keep the existing score
            status: "waiting", // Update the status to 'waiting'
          }),
        }
      );

      // Handle response from the backend
      const updateData = await updateResponse.json();
      console.log(updateData);

      // Check for the opposite match
      const oppositeMatch = matchesData.find(
        (m) =>
          m.user_1_id === currentDisplayedUser.user_data_id &&
          m.user_2_id === activeUser.user_data_id
      );

      if (oppositeMatch && oppositeMatch.status === "waiting") {
        // If both matches are in 'waiting' status, update both to 'accepted'
        const updateOppositeMatchResponse = await fetch(
          `http://localhost:5001/api/matches/${oppositeMatch.match_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user_1_id: oppositeMatch.user_1_id,
              user_2_id: oppositeMatch.user_2_id,
              match_score: oppositeMatch.match_score,
              status: "accepted", // Update the status to 'accepted'
            }),
          }
        );

        const updateOppositeMatchData = await updateOppositeMatchResponse.json();
        console.log(updateOppositeMatchData);

        // Update the original match to 'accepted' as well
        const updateOriginalMatchResponse = await fetch(
          `http://localhost:5001/api/matches/${match.match_id}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user_1_id: match.user_1_id,
              user_2_id: match.user_2_id,
              match_score: match.match_score,
              status: "accepted", // Update the status to 'accepted'
            }),
          }
        );

        const updateOriginalMatchData = await updateOriginalMatchResponse.json();
        console.log(updateOriginalMatchData);
      }

      // Set a random emoji
      setRandomEmoji(getRandomEmoji());

      // Trigger the heart animation
      setShowHeart(true);

      // Remove the current user from the displayedUsers list
      setDisplayedUsers((prevUsers) =>
        prevUsers.filter((user) => user.user_data_id !== currentDisplayedUser.user_data_id)
      );

      // Navigate to the next user
      setCurrentIndex((prevIndex) => {
        const allUsers = [...displayedUsers];
        let nextIndex = (prevIndex + 1) % allUsers.length; // Calculate next index
        setCurrentDisplayedUser(allUsers[nextIndex]); // Update currentDisplayedUser
        return nextIndex; // Return the new index
      });

      // Hide the heart after the animation completes
      setTimeout(() => {
        setShowHeart(false);
      }, 1000); // Adjust the timeout to match the animation duration
    } catch (error) {
      console.error("Error:", error);
    }
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
    <section className="mt-10 text-center" style={style}>
      {/* Emoji Animation */}
      {showHeart && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="heart-animation">{randomEmoji}</div>
        </div>
      )}

      <h2 className="mb-2 text-2xl font-semibold">A Display Caption?</h2>
      <p className="mb-4 text-base text-zinc-400">
        {currentDisplayedUser?.profile_name || "Person's Name"}
      </p>
      <div className="mx-auto mt-0 mb-5 w-full">
        {/* Seek bar */}
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
        {/* Time display */}
        <div className="flex justify-between text-xs text-zinc-400">
          <span>{formatTime(currentTime)}</span>
          <span>-{formatTime(totalDuration - currentTime)}</span>
        </div>
      </div>
      {/* Player controls */}
      <div className="flex gap-11 justify-center items-center max-sm:gap-8">
        {/* Previous button */}
        <div
          className="cursor-pointer focus:outline-none hover:scale-90 transition-transform duration-200"
          aria-label="Previous track"
          onClick={handlePreviousUser}
        >
          <PrevButton className="w-8 h-8" />
        </div>
        {/* Play button */}
        <div
          className="cursor-pointer focus:outline-none relative"
          aria-label="Play"
          onClick={handlePlay}  // Attach the handlePlay function
          onMouseEnter={() => setIsHoveringPlayButton(true)}
          onMouseLeave={() => setIsHoveringPlayButton(false)}
        >
          <div className="absolute inset-0 flex items-center justify-center z-0">
            <div className="w-8 h-8 bg-red-500 rounded-full opacity-0 hover:opacity-100 transition-opacity duration-200" />
          </div>
          <div className="relative z-10">
            {isHoveringPlayButton ? (
              <RedPlayButton className="w-10 h-10" />
            ) : (
              <PlayButton className="w-12 h-12" />
            )}
          </div>
        </div>

        {/* Next button */}
        <div
          className="cursor-pointer focus:outline-none hover:scale-90 transition-transform duration-200"
          aria-label="Next track"
          onClick={handleNextUser}
        >
          <NextButton className="w-8 h-8" />
        </div>
      </div>
    </section>
  );
}