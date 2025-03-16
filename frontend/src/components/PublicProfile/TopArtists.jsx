import React, { useEffect, useState } from "react";

const ArtistItem = ({ image, name }) => {
  return (
    <article className="flex gap-2.5 items-center">
      <img src={image} alt={name} className="object-cover w-12 h-12 rounded-full" />
      <h3 className="text-base font-medium tracking-tight leading-7 text-white max-sm:text-sm">
        {name}
      </h3>
    </article>
  );
};

export const TopArtists = () => {
  const [artists, setArtists] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5001/api/user_data")
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          const user = data[0]; // Assuming the first user for now
          const artistNames = user.top_artists ? user.top_artists.split(", ") : [];
          const artistImages = user.top_artists_pictures ? user.top_artists_pictures.split(", ") : [];

          // Combine names and images into artist objects
          const artistList = artistNames.map((name, index) => ({
            name,
            image: artistImages[index] || "https://via.placeholder.com/50", // Fallback image if missing
          }));

          setArtists(artistList.slice(0, 5)); // Limit to top 5 artists
        }
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <section className="flex flex-col gap-5">
      <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
        Top 5 Artists
      </h2>
      <div className="flex flex-col gap-5">
        {artists.map((artist, index) => (
          <ArtistItem key={index} {...artist} />
        ))}
      </div>
      <div className="h-1"></div> {/* Adds spacing below TopArtists */}
    </section>
  );
};
