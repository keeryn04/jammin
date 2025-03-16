import React from "react";
import MatchCard from "./MatchCard";

const matches = [
  {
    id: 1,
    name: "Sofia",
    age: 23,
    genre: "Jazz & Chill",
    image:
      "https://cdn.builder.io/api/v1/image/assets/TEMP/f76616cfec20ed2df0afb1bca88089e8b44c1633",
  },
  {
    id: 2,
    name: "William",
    age: 25,
    genre: "Rap & Hip-Hop",
    image:
      "https://cdn.builder.io/api/v1/image/assets/TEMP/0e18527866ca17b10e2cc10b8324a3922fd459a8",
  },
  {
    id: 3,
    name: "Lucas",
    age: 26,
    genre: "Rock & Alternative",
    image:
      "https://cdn.builder.io/api/v1/image/assets/TEMP/35c226df46915238c24c3528c9b3eae1e1f37628",
  },
  {
    id: 4,
    name: "Ava",
    age: 25,
    genre: "Indie & Jazz",
    image:
      "https://cdn.builder.io/api/v1/image/assets/TEMP/cea718ed1cd1a5b246775ef58cfc55fb0ef04fa5",
  },
  {
    id: 5,
    name: "Mia",
    age: 24,
    genre: "Pop & EDM",
    image:
      "https://cdn.builder.io/api/v1/image/assets/TEMP/d85b697bd4e17ea5e65907ce51ce16c393da43d1",
  },
];

const MatchesList = () => {
  return (
    <section className="flex-1 p-8 max-sm:p-4">
      <h1 className="mb-10 text-4xl font-bold text-white max-sm:mb-5 max-sm:text-3xl">
        Your Matches
      </h1>
      <div className="flex flex-col gap-4">
        {matches.map((match) => (
          <MatchCard key={match.id} {...match} />
        ))}
      </div>
    </section>
  );
};

export default MatchesList;
