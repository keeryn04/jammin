import { useState, useEffect } from "react";
import MediaSection from "./MediaSection";

// Import images from the assets folder
import mainImage from "./assets/main-image.jpg";
import image1 from "./assets/image1.jpg";
import image2 from "./assets/image2.jpg";
import image3 from "./assets/image3.jpg";
import image4 from "./assets/image4.jpeg";

const MediaSectionContainer = ({ type, title }) => {
  const [images, setImages] = useState([]);
  const [mainImage, setMainImage] = useState(""); // Keeps the main image
  const [songNames, setSongNames] = useState([]);
  const [artistNames, setArtistNames] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/user_data")
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          const user = data[0]; // Assume first user for now
          if (type === "songs") {
            const fetchedImages = user.top_songs_pictures ? user.top_songs_pictures.split(", ") : [];
            console.log(fetchedImages);
            setImages(fetchedImages);
            
            setSongNames(user.top_songs ? user.top_songs.split(", ") : []);
            setArtistNames(user.top_artists ? user.top_artists.split(", ") : []);
          } else if (type === "artists") {
            setImages(user.top_artists_pictures ? user.top_artists_pictures.split(", ") : []);
            setArtistNames(user.top_artists ? user.top_artists.split(", ") : []);
            console.log("Song Names: ", songNames);
            console.log("Artist Names: ", artistNames);
          }
        }
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, [type]);

  // After images are set, update the main image
  useEffect(() => {
    if (images.length > 0) {
      setMainImage(images[0]); // Set the first image as the main image
    }
  }, [images]); // Only run when images state updates

  return (
    <div className="flex-shrink-0 w-[400px] h-full">
      <MediaSection
        title={title}
        type={type}
        mainImage={mainImage || "https://variety.com/wp-content/uploads/2018/10/ninja_photo-credit-ryan-taylor_red-bull-content-pool.jpg"} // Fallback to image1 if mainImage is not set
        gridImages={images.length > 1 ? images.slice(1, 5) : [
          image1,
          image2,
          image3,
          image4,
        ]}
        songNames={songNames}
        artistNames={artistNames}
      />
    </div>
  );
};

export default MediaSectionContainer;
