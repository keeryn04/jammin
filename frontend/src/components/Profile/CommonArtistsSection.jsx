import React from "react";
import CommonArtist from "./CommonArtist"; // Import the CommonArtist component
import image4 from "./assets/image4.webp"; // Import the image

const CommonArtistsSection = () => {
  // Example data (replace with dynamic data from props or API)
  const artists = [
    { id: 1, name: "Artist 1", imageUrl: image4 },
    { id: 2, name: "Artist 2", imageUrl: image4 },
    { id: 3, name: "Artist 3", imageUrl: image4 },
    { id: 4, name: "Artist 4", imageUrl: image4 },
    { id: 5, name: "Artist 5", imageUrl: image4 },
    { id: 6, name: "Artist 6", imageUrl: image4 },
  ];

  return (
    <section className="px-0 py-4 w-[400px] max-md:w-full">
      <h2 className="mb-12 text-base leading-6 text-center text-white">
        Artists in Common
      </h2>
      <div className="overflow-y-auto max-h-[300px] p-4 [&::-webkit-scrollbar]:w-2
  [&::-webkit-scrollbar-track]:rounded-full
  [&::-webkit-scrollbar-track]:bg-gray-100
  [&::-webkit-scrollbar-thumb]:rounded-full
  [&::-webkit-scrollbar-thumb]:bg-gray-300
  dark:[&::-webkit-scrollbar-track]:bg-neutral-700
  dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500"> {/* Scrollable container */}
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