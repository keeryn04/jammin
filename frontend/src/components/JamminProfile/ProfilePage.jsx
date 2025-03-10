"use client";
import React from "react";
import Sidebar from "./Sidebar";
import ProfileContent from "./ProfileContent";

const ProfilePage = () => {
  return (
    <main className="flex min-h-screen bg-neutral-800">
      <Sidebar />
      <ProfileContent />
    </main>
  );
};

export default ProfilePage;
