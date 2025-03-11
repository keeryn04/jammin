"use client";
import React from "react";
import ProfileSection from "./ProfileSection";
import MediaSectionContainer from "./MediaSectionContainer"; // Updated Import
import GenreSection from "./GenreSection";
import CommonArtistsSection from "./CommonArtistsSection";

const SpotifyProfile = () => {
  return (
    <div className="flex space-x-4 p-4 w-max h-[400px] -ml-3">
      {/* Profile Section */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <ProfileSection />
      </div>

      {/* Media Section - Top Songs */}
      <MediaSectionContainer type="songs" title="Top Songs" />

      {/* Media Section - Top Artists */}
      <MediaSectionContainer type="artists" title="Top Artists" />

      {/* Genre Section */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <GenreSection />
      </div>

      {/* Common Artists Section */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <CommonArtistsSection />
      </div>
    </div>
  );
};

export default SpotifyProfile;
