import React from "react";
import MediaGrid from "./MediaGrid";

const MediaSection = ({ title, type, mainImage, gridImages, songNames = [], artistNames = [] }) => {
  return (
    <section className="px-0 py-4 w-[400px] max-md:w-full">
      <h2 className="mb-12 text-base leading-6 text-center text-white">
        {title}
      </h2>
      <div className="flex p-4 h-[215px]">
        {/* Main Image */}
        <div className="relative group">
          <img
            src={mainImage}
            alt={`Main ${type}`}
            className="h-[183px] w-[184px] object-cover rounded-tl-lg rounded-bl-lg"
          />

          {/* Hover Overlay for Main Image */}
          <div className="absolute inset-0 bg-black opacity-0 group-hover:opacity-50 transition-all duration-200 flex flex-col justify-center items-center rounded-tl-lg rounded-bl-lg">
            {type === "songs" && (
              <div className="text-center opacity-0 group-hover:opacity-100 transition-all duration-200">
                <p className="text-white text-lg font-bold">{songNames[0] || "Song Name"}</p>
              </div>
            )}
            {type === "artists" && (
              <div className="text-center opacity-0 group-hover:opacity-100 transition-all duration-200">
                <p className="text-white text-lg font-bold">{artistNames[0] || "Artist Name"}</p>
              </div>
            )}
          </div>
        </div>

        {/* Media Grid */}
        <MediaGrid images={gridImages} type={type} songNames={songNames.slice(1, 5)} artistNames={artistNames.slice(1, 5)} />
      </div>
    </section>
  );
};

export default MediaSection;
