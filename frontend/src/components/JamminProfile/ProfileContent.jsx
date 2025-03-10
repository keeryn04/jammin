import React from "react";
import PhotoSection from "./PhotoSection";
import ProfileForm from "./ProfileForm";

const ProfileContent = () => {
  return (
    <section className="flex-1 px-10 py-20 max-md:px-5 max-md:py-10 max-sm:p-5">
      <header className="flex justify-center items-center gap-10 py-10 text-center max-md:flex-col max-md:gap-5">
        <h1 className="text-2xl font-bold text-gray-400 hover:text-teal-400 max-sm:text-xl cursor-pointer">
            Public Profile
        </h1>
        <h2 className="text-2xl font-bold text-teal-400 transition-colors duration-200 max-sm:text-xl underline  cursor-pointer">
            Jammin' Profile
        </h2>
        </header>
      <div className="pl-80 max-md:pl-40">
        <PhotoSection />
        <ProfileForm />
      </div>
    </section>
  );
};

export default ProfileContent;
