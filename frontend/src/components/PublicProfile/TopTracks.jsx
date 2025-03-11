import React, { useEffect, useState } from "react";

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

export const TopTracks = () => {
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/user_data")
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          const user = data[0]; // Assuming the first user for now
          const songNames = user.top_songs ? user.top_songs.split(", ") : [];
          const songImages = user.top_songs_pictures ? user.top_songs_pictures.split(", ") : [];

          // Combine names and images into song objects
          const songList = songNames.map((name, index) => ({
            name,
            image: songImages[index] || "https://via.placeholder.com/50", // Fallback image if missing
          }));

          setSongs(songList.slice(0, 5)); // Limit to top 5 songs
        }
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <section className="flex flex-col gap-5">
      <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
        Top 5 Songs
      </h2>
      <div className="flex flex-col gap-5">
        {songs.map((song, index) => (
          <SongItem key={index} {...song} />
        ))}
      </div>
      <div className="h-1"></div> {/* Adds spacing below TopSongs */}
    </section>
  );
};
