import React, { useState } from "react";

const PhotoSection = () => {
  const [showMessage, setShowMessage] = useState(false);

  const handleClick = () => {
    setShowMessage(true);
    setTimeout(() => setShowMessage(false), 2000); // Hide the message after 2 seconds
  };

  return (
    <section>
      <h3 className="mb-6 text-2xl font-bold text-white">Photos</h3>
      <div className="grid gap-3.5 mb-16 grid-cols-[repeat(3,91px)] max-sm:grid-cols-[repeat(2,91px)]">
        {[...Array(6)].map((_, index) => (
          <div
            key={index}
            className="bg-white h-[91px] w-[91px] cursor-pointer"
            onClick={handleClick}
          />
        ))}
      </div>

      {/* Small, unintrusive pop-up message */}
      {showMessage && (
        <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-neutral-700 text-white px-4 py-2 rounded-lg shadow-lg text-sm">
          Coming Soon!
        </div>
      )}
    </section>
  );
};

export default PhotoSection;