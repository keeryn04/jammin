import React, { useEffect, useState, useContext } from "react";
import GenreCard from "./GenreCard";
import { UserContext } from "../UserContext";

const GenreSection = () => {
  const [genres, setGenres] = useState([]);
  // Access context values
  const { currentDisplayedUser } = useContext(UserContext);

  useEffect(() => {
    const topGenres = currentDisplayedUser.top_genres
      ? currentDisplayedUser.top_genres.split(", ")
      : [];
    setGenres(topGenres);
  }, [currentDisplayedUser]);

  return (
    <section className="px-0 py-4 w-[400px] max-md:w-full">
      <h2 className="mb-4 text-base leading-6 text-center text-white">
        Top Genres
      </h2>
      <div className="grid grid-cols-2 gap-3 p-4">
        {genres.slice(0, 6).map((genre, index) => (
          <GenreCard key={index} genre={genre} />
        ))}
      </div>
    </section>
  );
};

export default GenreSection;