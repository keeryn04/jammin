"use client";
import NavigationBar from "../Dashboard/Sidebar";
import { ProfileHeader } from "./ProfileHeader";
import { ProfilePhoto } from "./ProfilePhoto";
import { TopTracks } from "./TopTracks";
import { TopArtists } from "./TopArtists";
import { Prompts } from "./Prompts";

const ProfileLayout = () => {
  return (
    <div className="flex h-screen w-screen bg-neutral-800 overflow-hidden">
      {/* Navigation Bar (Fixed to the Left) */}
      <div className="h-full w-[152px] flex-none max-md:w-20 max-sm:w-[60px]">
        <NavigationBar />
      </div>

      {/* Main Content (Flexible and Scrollable) */}
      <main className="flex flex-1 flex-col overflow-hidden px-8 py-6 max-md:px-4">
        {/* Profile Header (Consistent Positioning) */}
        <div className="flex-shrink-0 w-full flex justify-center mb-6">
          <ProfileHeader />
        </div>

        {/* Scrollable Content */}
        <div className="flex flex-1 gap-10 p-6 rounded-lg bg-neutral-900 shadow-lg overflow-y-auto max-md:flex-col max-md:gap-5 max-md:p-4 [&::-webkit-scrollbar]:w-2
  [&::-webkit-scrollbar-track]:rounded-full
  [&::-webkit-scrollbar-track]:bg-gray-100
  [&::-webkit-scrollbar-thumb]:rounded-full
  [&::-webkit-scrollbar-thumb]:bg-gray-300
  dark:[&::-webkit-scrollbar-track]:bg-neutral-700
  dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500">
          {/* Left Column */}
          <div className="flex flex-col gap-10 flex-1 min-w-0">
            <ProfilePhoto />
            <TopTracks />
            <TopArtists />
          </div>

          {/* Right Column */}
          <aside className="flex flex-col gap-6 flex-1 min-w-0 max-w-full p-4">
            <Prompts />
          </aside>
        </div>
      </main>
    </div>
  );
};

export default ProfileLayout;
