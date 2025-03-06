import React from "react";

// Import images from the assets folder
import mainImage from "./assets/main-image.jpg";
import image1 from "./assets/image1.jpg";
import image2 from "./assets/image2.jpg";
import image3 from "./assets/image3.jpg";
import image4 from "./assets/image4.jpeg";

const MediaSection = ({ title, type }) => {
  // Define the grid images array
  const gridImages = [image1, image2, image3, image4];

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
                <p className="text-white text-lg font-bold">Song Name</p>
                <p className="text-gray-300 text-sm">Artist Name</p>
              </div>
            )}
            {type === "artists" && (
              <div className="text-center opacity-0 group-hover:opacity-100 transition-all duration-200">
                <p className="text-white text-lg font-bold">Artist Name</p>
              </div>
            )}
          </div>
        </div>

        {/* Media Grid */}
        <div className="grid grid-cols-2 grid-rows-2 gap-1 ml-1">
          {gridImages.map((image, index) => (
            <div key={index} className="relative group">
              {/* Image */}
              <img
                src={image}
                alt={`${type} ${index + 1}`}
                className={`h-[90px] w-[88px] object-cover ${
                  index === 1
                    ? "rounded-tr-lg" // Top-right corner rounded for top-right image
                    : index === 3
                    ? "rounded-br-lg" // Bottom-right corner rounded for bottom-right image
                    : ""
                }`}
              />

              {/* Hover Overlay */}
              <div
                className={`absolute inset-0 bg-black opacity-0 group-hover:opacity-50 transition-all duration-200 flex flex-col justify-center items-center ${
                  index === 1
                    ? "rounded-tr-lg" // Match rounded corners for overlay
                    : index === 3
                    ? "rounded-br-lg"
                    : ""
                }`}
              >
                {type === "songs" && (
                  <div className="text-center opacity-0 group-hover:opacity-100 transition-all duration-200">
                    <p className="text-white text-lg font-bold">
                      Song {index + 1}
                    </p>
                    <p className="text-gray-300 text-sm">Artist {index + 1}</p>
                  </div>
                )}
                {type === "artists" && (
                  <div className="text-center opacity-0 group-hover:opacity-100 transition-all duration-200">
                    <p className="text-white text-lg font-bold">
                      Artist {index + 1}
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default MediaSection;