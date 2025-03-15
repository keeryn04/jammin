import React, { useContext } from "react";
import { UserContext } from "../UserContext"; // Import the context
import CommonArtist from "./CommonArtist"; // Import the CommonArtist component
import image4 from "./assets/image4.webp"; // Import the image

const CommonArtistsSection = () => {
  const { currentDisplayedUser, displayedUsersChat, activeUser } = useContext(UserContext);

  // Find the match data for the currently displayed user
  const currentMatch = displayedUsersChat.find(
    (match) => match.userID === currentDisplayedUser?.user_data_id
  );

  // Extract common artists and songs
  const commonArtists = currentMatch?.common_top_artists || [];
  const commonSongs = currentMatch?.common_top_songs || [];

  // Combine common artists and songs into a single list for display
  const artists = commonArtists.map((artist, index) => ({
    id: index,
    name: artist,
    imageUrl: image4, // Use a placeholder image or fetch actual artist images
  }));

  return (
    <section className="px-0 py-4 w-[400px] max-md:w-full">
      <h2 className="mb-12 text-base leading-6 text-center text-white">
        Artists in Common
      </h2>
      <div
        className="overflow-y-auto max-h-[300px] p-4 [&::-webkit-scrollbar]:w-2
  [&::-webkit-scrollbar-track]:rounded-full
  [&::-webkit-scrollbar-track]:bg-gray-100
  [&::-webkit-scrollbar-thumb]:rounded-full
  [&::-webkit-scrollbar-thumb]:bg-gray-300
  dark:[&::-webkit-scrollbar-track]:bg-neutral-700
  dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500"
      >
        {" "}
        {/* Scrollable container */}
        <div className="grid gap-5 justify-center grid-cols-[repeat(2,128px)] max-sm:gap-4 max-sm:grid-cols-[1fr]">
          {artists.map((artist) => (
            <CommonArtist
              key={artist.id}
              name={artist.name}
              imageUrl={artist.imageUrl}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default CommonArtistsSection;