const MediaGrid = ({ images, type, songNames = [], artistNames = [] }) => {
    return (
      <div className="grid grid-cols-[repeat(2,88px)] grid-rows-[repeat(2,90px)] gap-1 ml-1">
        {images.map((image, index) => (
          <div key={index} className="relative group">
            {/* Image */}
            <img
              src={image}
              alt={`${type} ${index + 1}`}
              className={`h-[90px] w-[88px] object-cover ${
                index === 1 ? "rounded-tr-lg" : index === 3 ? "rounded-br-lg" : ""
              }`}
            />
  
            {/* Hover Overlay */}
            <div className="absolute inset-0 bg-black opacity-0 group-hover:opacity-50 transition-all duration-200 flex flex-col justify-center items-center">
              {/* Text for Top Songs */}
              {type === "songs" && (
                <div className="text-center opacity-0 group-hover:opacity-100 transition-all duration-200">
                  <p className="text-white text-sm font-bold">
                    {songNames[index] || "Song Name"}
                  </p>
                </div>
              )}
  
              {/* Text for Top Artists */}
              {type === "artists" && (
                <div className="text-center opacity-0 group-hover:opacity-100 transition-all duration-200">
                  <p className="text-white text-lg font-bold">
                    {artistNames[index] || "Artist Name"}
                  </p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    );
  };
  
  export default MediaGrid;