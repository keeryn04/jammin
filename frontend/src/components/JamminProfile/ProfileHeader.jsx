import React from "react";
import { Link } from "react-router-dom";

export const ProfileHeader = () => {
  return (
    <header className="flex justify-center items-center gap-10 py-10 text-center max-md:flex-col max-md:gap-5">
      <Link to="/PublicProfile">
        <h1 className="text-2xl font-bold text-gray-400 hover:text-teal-400 transition-colors duration-200 max-sm:text-xl">
          Public Profile
        </h1>
      </Link>

      <h2 className="text-2xl font-bold text-teal-400 max-sm:text-xl underline">
        Jammin' Profile
      </h2>
    </header>
  );
};
