"use client";
import React from "react";
import ProfileSection from "./ProfileSection";
import MediaSectionContainer from "./MediaSectionContainer";
import GenreSection from "./GenreSection";
import CommonArtistsSection from "./CommonArtistsSection";

const SpotifyProfile = ({ activeUser, displayedUsers }) => {
  return (
    <div className="flex space-x-4 p-4 w-max h-[400px] -ml-3">
      {/* Profile Section */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <ProfileSection activeUser={activeUser} displayedUsers={displayedUsers} />
      </div>

      {/* Media Section - Top Songs */}
      <MediaSectionContainer type="songs" title="Top Songs" activeUser={activeUser} displayedUsers={displayedUsers} />

      {/* Media Section - Top Artists */}
      <MediaSectionContainer type="artists" title="Top Artists" activeUser={activeUser} displayedUsers={displayedUsers} />

      {/* Genre Section */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <GenreSection activeUser={activeUser} displayedUsers={displayedUsers} />
      </div>

      {/* Common Artists Section */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <CommonArtistsSection activeUser={activeUser} displayedUsers={displayedUsers} />
      </div>
    </div>
  );
};

export default SpotifyProfile;