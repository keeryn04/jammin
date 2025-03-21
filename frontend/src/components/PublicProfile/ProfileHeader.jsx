import React from 'react'
import { Link } from 'react-router-dom';

export const ProfileHeader = () => {
    return (
      <header className="flex justify-center items-center gap-10 py-10 text-center flex-row max-md:gap-5">
        
          <h1 className="text-2xl font-bold text-teal-400 max-sm:text-xl underline">
            Public Profile
          </h1>
        

        <Link to="/JamminProfile">
          <h2 className="text-2xl font-bold text-gray-400 hover:text-teal-400 transition-colors duration-200 cursor-pointer max-sm:text-xl">
            Jammin' Profile
          </h2>
        </Link>
        
      </header>
    );
  };
  