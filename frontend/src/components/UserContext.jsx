import React, { createContext, useState, useEffect } from "react";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [activeUser, setActiveUser] = useState(null);
  const [displayedUsers, setDisplayedUsers] = useState([]);
  const [displayedUsersChat, setDisplayedUsersChat] = useState([]); 
  const [displayedUserProfile, setDisplayedUserProfile] = useState([]); 
  const [currentDisplayedUser, setCurrentDisplayedUser] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [allUsersData, setAllUsersData] = useState([]);  // State to store all user data from users_music_data

  const VERCEL_URL = import.meta.env.VITE_VERCEL_URL;
  const userDataLink = `${VERCEL_URL}/api/user_data`;
  const cookieFetchLink = `${VERCEL_URL}/api/auth/check`;

  useEffect(() => {
  const fetchData = async () => {
      try {
        // Fetch the active user ID
        const res = await fetch(cookieFetchLink, { credentials: "include" });
        const data = await res.json();
        const userDataId = data.user.user_data_id
        console.log(data)
        
        if (!userDataId) {
          console.error("No active user data_id found");
          return;
        }

        // Fetch all user data from users_music_data
        const allUsersDataResponse = await fetch(userDataLink);
        const allUsersData = await allUsersDataResponse.json();
        console.log("All Users Data:", allUsersData);
        setAllUsersData(allUsersData);

        // Find the active user from all users data
        const activeUserData = allUsersData.find(
          (user) => user.user_data_id === userDataId
        );
        console.log("Active User Data:", activeUserData);
        setActiveUser(activeUserData);

        if (!activeUserData) {
          console.error("Active user not found in all users data.");
          return;
        }

        // Fetch compatibility matches for the active user
        const matchesResponse = await fetch(
          `${VERCEL_URL}/api/chattesting/${activeUserData.user_data_id}`
        );
        const matchesData = await matchesResponse.json();
        console.log("Matches Data:", matchesData);

        if (matchesData.matches) {
          setDisplayedUsersChat(matchesData.matches);

          // Extract user IDs from the matches
          const userDataIDs = matchesData.matches.map((match) => match.user_data_id);
          console.log("User IDs from Matches:", userDataIDs);

          // Find additional profile data for each matched user
          const profiles = userDataIDs.map((userDataId) =>
            allUsersData.find((user) => user.user_data_id === userDataId)
          );
          console.log("Profiles Data:", profiles);
          setDisplayedUserProfile(profiles);
          setDisplayedUsers(profiles);
          setCurrentDisplayedUser(profiles[0]);
          setCurrentIndex(0);
        } else {
          console.error("No matches found in the response.");
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []); // Re-run effect when activeUserId changes

  return (
    <UserContext.Provider
      value={{
        activeUser,
        displayedUsers,
        displayedUsersChat, // Provide compatibility data
        displayedUserProfile, // Provide additional profile data
        currentDisplayedUser,
        setCurrentDisplayedUser,
        currentIndex,
        setCurrentIndex,
        setActiveUser,
        setDisplayedUsers,
        allUsersData, // Provide all user data from users_music_data
      }}
    >
      {children}
    </UserContext.Provider>
  );
};