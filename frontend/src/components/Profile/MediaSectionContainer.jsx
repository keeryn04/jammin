import React, { useContext } from "react";
import { UserContext } from "../UserContext";
import MediaSection from "./MediaSection";

const MediaSectionContainer = ({ type, title }) => {
  const { currentDisplayedUser } = useContext(UserContext);

  // Ensure `images` is always an array
  const images =
    type === "songs"
      ? currentDisplayedUser?.top_songs_pictures?.split(", ") || []
      : currentDisplayedUser?.top_artists_pictures?.split(", ") || [];

  return (
    <div className="flex-shrink-0 w-[400px] h-full">
      <MediaSection
        title={title}
        type={type}
        mainImage={images[0] || "default-image.jpg"} // Fallback if no image
        gridImages={images.slice(1, 5)} // Ensure this is always an array
        songNames={currentDisplayedUser?.top_songs?.split(", ") || []}
        artistNames={currentDisplayedUser?.top_artists?.split(", ") || []}
      />
    </div>
  );
};

export default MediaSectionContainer;