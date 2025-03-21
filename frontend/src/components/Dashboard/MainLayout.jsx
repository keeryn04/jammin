"use client";
import React, { useRef, useState, useEffect, useContext } from "react";
import Sidebar from "./Sidebar";
import SpotifyProfile from "../Profile/SpotifyProfile";
import MusicPlayer from "./MusicPlayer";
import { UserContext } from "../UserContext"; // Import the context
import Loading from "../Loading/Loading";

export default function MainLayout() {
  const [currentTime, setCurrentTime] = useState(0);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const totalDuration = 260; // 4:20 in seconds
  const profileContainerRef = useRef(null);
  const [currentMatch, setCurrentMatch] = useState(null); // State to store the current match
  const [showHeart, setShowHeart] = useState(false); // State to control heart animation
  const [randomEmoji, setRandomEmoji] = useState(""); // State to store the random emoji
  const [isLoading, setIsLoading] = useState(true); // Loading state
  const [isOutOfMatches, setIsOutOfMatches] = useState(false);

  const VERCEL_URL = import.meta.env.VITE_VERCEL_URL;

  // Use a ref to track the previous displayed user
  const prevDisplayedUserRef = useRef();

  // Access context values
  const {
    activeUser,
    displayedUsers,
    setDisplayedUsers,
    currentDisplayedUser,
    setCurrentDisplayedUser,
    currentIndex,
    setCurrentIndex,
    displayedUsersChat,
  } = useContext(UserContext);

    // Update loading state when data is available
    useEffect(() => {
      const loadingTimeout = setTimeout(() => {
        if (isLoading) {
          setIsOutOfMatches(true); // Switch to "out of matches" if loading takes too long
          setIsLoading(false); // Stop loading
        }
      }, 20000); // 10 seconds
  
      // Cleanup the timer when the component unmounts or loading finishes
      return () => clearTimeout(loadingTimeout);
    }, [isLoading]);
  
    // Update loading state when data is available
    useEffect(() => {
      if (displayedUsers.length > 0 && displayedUsersChat.length > 0) {
        setIsLoading(false);
      }
    }, [displayedUsers, displayedUsersChat]);
  
    useEffect(() => {
      if (displayedUsers.length === 0 || displayedUsersChat.length === 0) {
        setIsOutOfMatches(true);
      } else {
        setIsOutOfMatches(false);
      }
    }, [displayedUsers, displayedUsersChat]);

  // Fetch all matches and find the desired match based on user IDs
  useEffect(() => {
    const fetchMatches = async () => {
      if (!activeUser || !currentDisplayedUser) return;

      try {
        const response = await fetch(`${VERCEL_URL}/api/matches`);
        if (response.ok) {
          const matches = await response.json();

          // Find the match where user_1_id and user_2_id match the active and displayed users
          const match = matches.find(
            (m) =>
              (m.user_1_data_id === activeUser.user_data_id &&
                m.user_2_data_id === currentDisplayedUser.user_data_id) ||
              (m.user_1_data_id === currentDisplayedUser.user_data_id &&
                m.user_2_data_id === activeUser.user_data_id)
          );

          setCurrentMatch(match); // Set the found match
        } else {
          console.error("Failed to fetch matches");
        }
      } catch (error) {
        console.error("Error fetching matches:", error);
      }
    };

    fetchMatches();
  }, [activeUser, currentDisplayedUser]); // Re-fetch when activeUser or currentDisplayedUser changes

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

    if (container && !isLoading && !isOutOfMatches) {
      container.addEventListener("scroll", handleScroll);
    }

    return () => {
      if (container) {
        container.removeEventListener("scroll", handleScroll);
      }
    };
  }, [totalDuration, isLoading, isOutOfMatches]); // Add isLoading and isOutOfMatches as dependencies

  // Toggle dropdown
  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  // Reset time when the displayed user changes
  useEffect(() => {
    if (prevDisplayedUserRef.current !== currentDisplayedUser) {
      handleSeek(0); // Reset time to 0:00
      prevDisplayedUserRef.current = currentDisplayedUser; // Update the ref
    }
  }, [currentDisplayedUser, handleSeek]);

  // Handle "Remove" button click
  const handleRemove = async () => {
    if (!currentMatch) {
      console.error("No match data available");
      return;
    }

    try {
      const updateResponse = await fetch(
        `${VERCEL_URL}/api/matches/${currentMatch.match_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_1_id: currentMatch.user_1_data_id,
            user_2_id: currentMatch.user_2_data_id,
            match_score: currentMatch.match_score, // Keep the existing score
            status: "rejected", // Update the status to 'rejected'
            reasoning: currentMatch.reasoning,
          }),
        }
      );

      if (updateResponse.ok) {
        console.log("Match status updated to 'rejected'");

        // Trigger the "X" emoji animation and navigate to the next user
        setRandomEmoji("❌"); // Set the "X" emoji
        setShowHeart(true); // Trigger the animation

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

        // Hide the "X" emoji after the animation completes
        setTimeout(() => {
          setShowHeart(false);
        }, 1000); // Adjust the timeout to match the animation duration
      } else {
        console.error("Failed to update match status");
      }
    } catch (error) {
      console.error("Error updating match status:", error);
    }
  };

  function setAppHeight() {
    const vh = window.visualViewport ? window.visualViewport.height : window.innerHeight;
    document.documentElement.style.setProperty('--app-height', `${vh}px`);
  }

  window.addEventListener('resize', setAppHeight);
  window.addEventListener('load', setAppHeight);
  setTimeout(setAppHeight, 50); // Small delay to allow UI adjustments

  return (
    <div className="flex flex-col sm:flex-row w-screen bg-neutral-800 h-[var(--app-height)] max-sm:items-center">

      {/* Sidebar */}
      <Sidebar />
      {/* Main content area */}
      <main className="flex-1 flex justify-center items-center sm:order-none order-first">
        <div className="w-[100%]">
            <h1 className="   m-5 text-6xl
                              font-bold text-left 
                              text-white max-w-[866px] 
                              max-md:max-w-[700px] 
                              max-sm:max-w-full 
                              ">
              Explore
            </h1>
          </div>
        {/* Centered content */}
        {isLoading ? (
          // Display the Loading component while data is being fetched
          <Loading />
        ) : isOutOfMatches ? (
          // Display the "out of users" message when there are no more users
          <div className="text-center">
            <h1 className="text-2xl font-afacad">Jam it! You're Out of Matches</h1>
            <p className="text-neutral-400">Come back later to see new matches!</p>
          </div>
        ) : (
          
          // Display the main content if there are users to match with
          <div className="flex flex-col items-center gap-2">
            {/* Header with "Jammin'" text and three-dot dropdown */}
            <div className="w-[90%] flex justify-between items-center mb-1">
              <h1 className="text-sm font-afacad text-center flex-1 text-white">Jammin'</h1>
              <div className="relative">
                <button onClick={toggleDropdown} className="text-white focus:outline-none">
                  &#8942; {/* Three dots */}
                </button>
                {isDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-28 bg-neutral-900 rounded-lg shadow-lg">
                    <ul>
                      <li
                        className="px-4 py-2 hover:bg-red-500 cursor-pointer rounded-md"
                        onClick={handleRemove}
                      >
                        Remove
                      </li>
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
            showHeart={showHeart}
            setShowHeart={setShowHeart}
            randomEmoji={randomEmoji}
            setRandomEmoji={setRandomEmoji}
          />
        </div>
        )}
      </main>

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
    </div>
  );
}