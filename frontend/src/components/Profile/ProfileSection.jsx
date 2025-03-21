"use client";
import React, { useState, useContext } from "react";
import { UserContext } from "../UserContext"; // Import the context
import ProgressBar from "./ProgressBar";

const ProfileSection = () => {
  const { currentDisplayedUser, displayedUsersChat } = useContext(UserContext); // Use the context

  const [isClicked, setIsClicked] = useState(false);

  const handleClick = () => {
    setIsClicked(!isClicked);
  };

  // Find the match data for the currently displayed user
  const currentMatch = displayedUsersChat.find(
    (match) => match.userID === currentDisplayedUser?.user_data_id
  );

  // Extract compatibility score and reasoning
  const compatibilityScore = currentMatch?.compatibility_score || 0;
  const reasoning = currentMatch?.reasoning || "No compatibility data available.";

  // Fallback values for missing data
  const profileImage = currentDisplayedUser?.profile_image || "default-profile.png";
  const profileName = currentDisplayedUser?.profile_name || "SpotifyUser";

  return (
    <section className="flex flex-col items-center p-4 w-[350px] relative overflow-hidden h-[350px]">
      {/* Progress Bar */}
      <div
        className={`p-4 w-full transition-all duration-500 ${
          isClicked
            ? "transform translate-y-0"
            : "transform translate-y-[calc(100%+8rem)]"
        }`}
        onClick={handleClick}
      >
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-base font-medium text-white">Compatibility Score</h2>
          <span className="text-sm text-white">{compatibilityScore}%</span>
        </div>
        <ProgressBar progress={compatibilityScore} />
      </div>

      {/* Profile Content */}
      <div
        className={`flex ${
          isClicked ? "flex-row items-start gap-4" : "flex-col items-center"
        } transition-all duration-500 ${
          isClicked ? "mt-4" : "mt-[-4rem]"
        }`}
      >
        <img
          src={profileImage}
          alt="Profile"
          className={`shadow-sm rounded-[99px] object-cover transition-all duration-500 ${
            isClicked ? "w-20 h-20" : "w-32 h-32"
          }`}
        />

        <div
          className={`text-center transition-all duration-500 ${
            isClicked ? "text-left" : ""
          }`}
        >
          <div className="text-[25px] font-bold leading-7 text-white">
            {profileName}
          </div>
          
          {/*
          <p className="text-base leading-6 text-gray-400">
            1 Followers · 1 Following
          </p>
          */}

          {/* Compatibility Text (Visible Only After Click) */}
          {isClicked && (
            <p className="mt-2 text-sm text-gray-300">
              {reasoning}
            </p>
          )}
        </div>
      </div>
    </section>
  );
};

export default ProfileSection;