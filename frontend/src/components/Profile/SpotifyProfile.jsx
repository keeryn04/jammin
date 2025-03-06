"use client";
import React from "react";
import ProfileSection from "./ProfileSection";
import MediaSection from "./MediaSection";
import GenreSection from "./GenreSection";
import CommonArtistsSection from "./CommonArtistsSection";

const SpotifyProfile = () => {
  return (
    <div className="flex space-x-4 p-4 w-max h-[400px] -ml-3"> {/* Added -ml-8 for negative margin-left */}
      {/* Profile Section */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <ProfileSection />
      </div>

      {/* Media Section - Top Songs */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <MediaSection
          title="Top Songs"
          mainImage="https://cdn.builder.io/api/v1/image/assets/TEMP/5a634914109b7aa569ee0c1bd19b5fd923fdb791"
          gridImages={[
            "https://cdn.builder.io/api/v1/image/assets/TEMP/2865ffc5e35560a47ed3e1e66e2f1a41a16a3f39",
            "https://cdn.builder.io/api/v1/image/assets/TEMP/b30cc3d7a02c52382c2b290666dcac8bb1898222",
            "https://cdn.builder.io/api/v1/image/assets/TEMP/69f9b11ed297528243a2b5a4431fd1a47b758d47",
            "https://cdn.builder.io/api/v1/image/assets/TEMP/4b7b4b2ce5a5a494de0c76fd713b5e363b459bc4",
          ]}
          type="songs"
        />
      </div>

      {/* Media Section - Top Artists */}
      <div className="flex-shrink-0 w-[400px] h-full">
        <MediaSection
          title="Top Artists"
          mainImage="https://cdn.builder.io/api/v1/image/assets/TEMP/560f4b1ce018ce9de36e0b200bef070cbe89efeb"
          gridImages={[
            "https://cdn.builder.io/api/v1/image/assets/TEMP/2865ffc5e35560a47ed3e1e66e2f1a41a16a3f39",
            "https://cdn.builder.io/api/v1/image/assets/TEMP/b30cc3d7a02c52382c2b290666dcac8bb1898222",
            "https://cdn.builder.io/api/v1/image/assets/TEMP/369c2f0d755a7eb59989eb73c5a418244b18ff5d",
            "https://cdn.builder.io/api/v1/image/assets/TEMP/f515732228dfb6b35b009c18f8c114a15d832914",
          ]}
          type="artists"
        />
      </div>

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