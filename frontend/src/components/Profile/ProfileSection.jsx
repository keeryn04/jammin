import React, { useEffect, useState } from "react";
import ProgressBar from "./ProgressBar";

const fetchLink = "http://localhost:5000/api/user_data";

const ProfileSection = () => {
  const [profileName, setProfileName] = useState("");
  const [profileImage, setProfileImage] = useState("");

  useEffect(() => {
    // Example of fetching user data from an API (replace with your actual endpoint)
    fetch(fetchLink)
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          const user = data[0]; // Assuming the first user for now
          setProfileName(user.profile_name || "SpotifyUser"); // Default if not found
          setProfileImage(user.profile_image || "default-profile.png"); // Default if not found
        }
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const [isClicked, setIsClicked] = useState(false);

  const handleClick = () => {
    setIsClicked(!isClicked);
  };

  return (
    <section className="flex flex-col items-center p-4 w-[400px] max-md:w-full relative overflow-hidden min-h-[400px]">
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
          <span className="text-sm text-white">85%</span>
        </div>
        <ProgressBar progress={85} />
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
          className={`shadow-sm rounded-[99px] transition-all duration-500 ${
            isClicked ? "w-20 h-20" : "w-32 h-32"
          }`}
        />
        <div
          className={`text-center transition-all duration-500 ${
            isClicked ? "text-left" : ""
          }`}
        >
          <div className="text-[25px] font-bold leading-7 text-white">
            {profileName || "SpotifyUser"}
          </div>
          <p className="text-base leading-6 text-gray-400">
            1 Followers · 1 Following
          </p>
          {/* Compatibility Text (Visible Only After Click) */}
          {isClicked && (
            <p className="mt-2 text-sm text-gray-300">
              Your compatibility score is based on shared music tastes, favorite
              artists, and listening habits. You both love indie rock and have
              similar top tracks!
            </p>
          )}
        </div>
      </div>
    </section>
  );
};

export default ProfileSection;
