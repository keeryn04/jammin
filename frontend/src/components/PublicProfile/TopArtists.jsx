import React from "react";

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

export const TopArtists = ({ activeUser }) => {
  const artistNames = activeUser?.top_artists ? activeUser.top_artists.split(", ") : [];
  const artistImages = activeUser?.top_artists_pictures ? activeUser.top_artists_pictures.split(", ") : [];

  // Combine names and images into artist objects
  const artists = artistNames.map((name, index) => ({
    name,
    image: artistImages[index] || "https://via.placeholder.com/50", // Fallback image if missing
  }));

  return (
    <section className="flex flex-col gap-5">
      <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
        Top 5 Artists
      </h2>
      <div className="flex flex-col gap-5">
        {artists.slice(0, 5).map((artist, index) => (
          <ArtistItem key={index} {...artist} />
        ))}
      </div>
      <div className="h-1"></div> {/* Adds spacing below TopArtists */}
    </section>
  );
};