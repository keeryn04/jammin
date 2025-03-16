import React from "react";

const PhotoSection = () => {
  return (
    <section>
      <h3 className="mb-6 text-2xl font-bold text-white">Photos</h3>
      <div className="grid gap-3.5 mb-16 grid-cols-[repeat(3,91px)] max-sm:grid-cols-[repeat(2,91px)]">
        {[...Array(6)].map((_, index) => (
          <div key={index} className="bg-white h-[91px] w-[91px]" />
        ))}
      </div>
    </section>
  );
};

export default PhotoSection;
