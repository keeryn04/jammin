import React from "react";
import CompatibilityScore from "./CompatibilityScore";

export default function ProfileCard() {
  return (
    <section className="p-5 mx-auto my-0 rounded-lg bg-neutral-900 max-w-[400px] max-sm:p-4">
      <div className="flex flex-col items-center text-center">
        <img
          src="https://cdn.builder.io/api/v1/image/assets/TEMP/484821ff3482c725dad0163a97077dd7b94e2dbd"
          alt="Profile"
          className="mb-4 w-32 h-32 rounded-full shadow-[0_4px_4px_rgba(0,0,0,0.25)] max-sm:h-[100px] max-sm:w-[100px]"
        />
        <div>
          <h1 className="mb-1 text-2xl font-bold max-sm:text-lg">
            SpotifyUser
          </h1>
          <p className="text-base text-gray-400 max-sm:text-sm">
            1 Followers · 1 Following
          </p>
        </div>
      </div>
      <CompatibilityScore score={85} />
    </section>
  );
}
