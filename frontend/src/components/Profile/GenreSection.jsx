import React, { useEffect, useState, useContext } from "react";
import GenreCard from "./GenreCard";
import { UserContext } from "../UserContext";

const GenreSection = () => {
  const [genres, setGenres] = useState([]);
    // Access context values
    const {
      currentDisplayedUser,
    } = useContext(UserContext);

    useEffect(() => {
      console.log("GENRESSS", currentDisplayedUser);
      const topGenres = currentDisplayedUser.top_genres ? currentDisplayedUser.top_genres.split(", ") : [];
      setGenres(topGenres);
    }, [currentDisplayedUser]);

  return (
    <section className="px-0 py-4 w-[400px] max-md:w-full">
      <h2 className="mb-12 text-base leading-6 text-center text-white">
        Top Genres
      </h2>
      <div className="flex flex-col gap-3 p-4">
        {[0, 1, 2].map((rowIndex) => (
          <div
            key={rowIndex}
            className="flex gap-3 justify-between max-sm:flex-col"
          >
            <GenreCard genre={genres[rowIndex * 2]} />
            <GenreCard genre={genres[rowIndex * 2 + 1]} />
          </div>
        ))}
      </div>
    </section>
  );
};

export default GenreSection;