"use client";
import React from "react";
import ProfileContent from "./ProfileContent";
import NavigationBar from "../Dashboard/Sidebar";

const ProfilePage = () => {
  return (
    <main className="flex h-screen w-screen bg-neutral-800 overflow-hidden">
      <NavigationBar />
      <ProfileContent />
    </main>
  );
};

export default ProfilePage;
