import React, { useEffect, useState } from "react";
import GenreCard from "./GenreCard";

const GenreSection = () => {
  const [genres, setGenres] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5001/api/user_data")
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          const user = data[0]; // Assuming the first user for now
          const topGenres = user.top_genres ? user.top_genres.split(", ") : [];
          setGenres(topGenres);
        }
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

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
