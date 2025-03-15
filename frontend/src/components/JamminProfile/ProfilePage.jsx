"use client";
import React, { useContext } from "react";
import { UserContext } from "../UserContext"; // Adjust the path as needed
import ProfileContent from "./ProfileContent";
import NavigationBar from "../Dashboard/Sidebar";

const ProfilePage = () => {
  const { activeUser } = useContext(UserContext); // Consume the context

  if (!activeUser) {
    return <div>Loading...</div>; // Add a loading state
  }

  return (
    <main className="flex h-screen w-screen bg-neutral-800 overflow-hidden">
      <NavigationBar />
      <ProfileContent activeUser={activeUser} /> {/* Pass activeUser as a prop */}
    </main>
  );
};

export default ProfilePage;