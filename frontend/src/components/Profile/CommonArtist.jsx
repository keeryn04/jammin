import React from "react";

const CommonArtist = ({ name, imageUrl }) => (
  <article className="text-center cursor-pointer group">
    <img
      src={imageUrl}
      alt={name}
      className="w-32 h-32 shadow-sm rounded-[99px] transition-transform duration-300 group-hover:scale-105"
    />
    <h3 className="mt-2 text-base font-bold text-white transition-all duration-300 group-hover:underline">
      {name}
    </h3>
  </article>
);

export default CommonArtist;