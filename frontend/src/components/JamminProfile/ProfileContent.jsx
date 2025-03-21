import React from "react";
import PhotoSection from "./PhotoSection";
import ProfileForm from "./ProfileForm";
import { ProfileHeader } from "./ProfileHeader";

const ProfileContent = ({ activeUser }) => {
  return (
    <div className="flex flex-1 flex-col sm:w-screen flex-grow items-center sm:order-none order-first
     overflow-y-auto [&::-webkit-scrollbar]:w-2
      [&::-webkit-scrollbar-track]:rounded-full
      [&::-webkit-scrollbar-track]:bg-gray-100
      [&::-webkit-scrollbar-thumb]:rounded-full
      [&::-webkit-scrollbar-thumb]:bg-gray-300
      dark:[&::-webkit-scrollbar-track]:bg-neutral-700
      dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500">
      {/* Main Content (Flexible and Scrollable) */}
      <main className="flex flex-1 flex-col overflow-hidden px-8 py-6 max-md:px-4">
        {/* Profile Header (Consistent Positioning) */}
        <div className="flex-shrink-0 w-full flex justify-center mb-6">
          <ProfileHeader />
        </div>

        {/* Scrollable Content */}
        <div className="flex flex-1 justify-center p-6 rounded-lg bg-neutral-900 shadow-lg overflow-y-auto max-md:p-4 max-md:flex-col [&::-webkit-scrollbar]:w-2
        [&::-webkit-scrollbar-track]:rounded-full
        [&::-webkit-scrollbar-track]:bg-gray-100
        [&::-webkit-scrollbar-thumb]:rounded-full
        [&::-webkit-scrollbar-thumb]:bg-gray-300
        dark:[&::-webkit-scrollbar-track]:bg-neutral-700
        dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500">
          <div className="max-w-[800px] w-full flex flex-col gap-10">
          {/* <PhotoSection activeUser={activeUser} /> */}
            <ProfileForm activeUser={activeUser} /> {/* Pass activeUser */}
          </div>
        </div>
      </main>
    </div>
  );
};

export default ProfileContent;