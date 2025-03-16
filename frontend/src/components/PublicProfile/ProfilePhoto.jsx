import React, { useEffect, useState } from "react";

export const ProfilePhoto = () => {
  const [profileName, setProfileName] = useState("");
  const [profileImage, setProfileImage] = useState("");

  useEffect(() => {
    fetch("http://localhost:5001/api/user_data") // Replace with actual API URL
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          const user = data[0]; // Assuming first user
          setProfileName(user.profile_name || "SpotifyUser"); // Default if not found
          setProfileImage(user.profile_image || "default-profile.png"); // Default if not found
        }
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

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
