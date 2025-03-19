import React from "react";

export const ProfilePhoto = ({ activeUser }) => {
  const profileName = activeUser?.profile_name || "SpotifyUser"; // Fallback if not found
  const profileImage = activeUser?.profile_image || "https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small_2x/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg"; // Fallback if not found

  return (
    <section className="flex flex-col items-center gap-3">
      <h2 className="text-2xl font-bold text-white max-sm:text-xl">
        {profileName}
      </h2>
      <div className="w-16 h-16 overflow-hidden rounded-full border-2 border-white">
        <img
          src={profileImage}
          alt={profileName}
          className="object-cover w-full h-full"
        />
      </div>
    </section>
  );
};