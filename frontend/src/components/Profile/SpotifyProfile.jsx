"use client";
import React, { useContext } from "react";
import { UserContext } from "../UserContext"; // Import the context
import ProfileSection from "./ProfileSection";
import MediaSectionContainer from "./MediaSectionContainer";
import GenreSection from "./GenreSection";
import CommonArtistsSection from "./CommonArtistsSection";

const SpotifyProfile = () => {
  const {
    activeUser,
    displayedUsers,
    displayedUsersChat,
    currentDisplayedUser,
  } = useContext(UserContext);

  return (
    <div className="flex space-x-4 p-4 w-max h-[350px] -ml-3">
      {/* Profile Section */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <ProfileSection />
      </div>

      {/* Media Section - Top Songs */}
      <MediaSectionContainer
        type="songs"
        title="Top Songs"
        activeUser={activeUser}
        displayedUsers={displayedUsers}
        displayedUsersChat={displayedUsersChat}
        currentDisplayedUser={currentDisplayedUser}
      />

      {/* Media Section - Top Artists */}
      <MediaSectionContainer
        type="artists"
        title="Top Artists"
        activeUser={activeUser}
        displayedUsers={displayedUsers}
        displayedUsersChat={displayedUsersChat}
        currentDisplayedUser={currentDisplayedUser}
      />

      {/* Genre Section */}
      <div className="flex-shrink-0 w-[380px] h-full">
        <GenreSection />
      </div>

      {/* Common Artists Section */}
      {/*
      <div className="flex-shrink-0 w-[400px] h-full">
        <CommonArtistsSection />
      </div>
      */}
    </div>
  );
};

export default SpotifyProfile;