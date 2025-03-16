import React from "react";

const SongItem = ({ image, name }) => {
  return (
    <article className="flex gap-2.5 items-center">
      <img src={image} alt={name} className="object-cover w-12 h-12 rounded-full" />
      <h3 className="text-base font-medium tracking-tight leading-7 text-white max-sm:text-sm">
        {name}
      </h3>
    </article>
  );
};

export const TopTracks = ({ activeUser }) => {
  const songNames = activeUser?.top_songs ? activeUser.top_songs.split(", ") : [];
  const songImages = activeUser?.top_songs_pictures ? activeUser.top_songs_pictures.split(", ") : [];

  // Combine names and images into song objects
  const songs = songNames.map((name, index) => ({
    name,
    image: songImages[index] || "https://via.placeholder.com/50", // Fallback image if missing
  }));

  return (
    <section className="flex flex-col gap-5">
      <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
        Top 5 Songs
      </h2>
      <div className="flex flex-col gap-5">
        {songs.slice(0, 5).map((song, index) => (
          <SongItem key={index} {...song} />
        ))}
      </div>
      <div className="h-1"></div> {/* Adds spacing below TopSongs */}
    </section>
  );
};