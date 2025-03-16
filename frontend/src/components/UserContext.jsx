import React, { createContext, useState, useEffect } from "react";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [activeUser, setActiveUser] = useState(null);
  const [displayedUsers, setDisplayedUsers] = useState([]);
  const [displayedUsersChat, setDisplayedUsersChat] = useState([]); // For compatibility data
  const [displayedUserProfile, setDisplayedUserProfile] = useState([]); // For additional user profile data
  const [currentDisplayedUser, setCurrentDisplayedUser] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [allUsersData, setAllUsersData] = useState([]); // State to store all user data from users_music_data

  // Specify the user_data_id of the active user manually
  const activeUserId = "df3d8dca-01e8-11f0-9689-0242ac120002"; // Replace with your desired user_data_id

  // Fetch all user data from users_music_data and initialize displayed users
  useEffect(() => {
    const abortController = new AbortController(); // Create an AbortController

    const fetchAllUsersData = async () => {
      try {
        // Fetch all users from the users_music_data endpoint
        const allUsersDataResponse = await fetch(
          `http://localhost:5001/api/user_data`,
          { signal: abortController.signal } // Pass the abort signal
        );
        const allUsersData = await allUsersDataResponse.json();
        console.log("All Users Data (from users_music_data):", allUsersData); // Log all users data
        setAllUsersData(allUsersData);

        // Find the active user from the fetched data
        const activeUserData = allUsersData.find(
          (user) => user.user_data_id === activeUserId
        );
        console.log("Active User Data:", activeUserData); // Log active user data
        setActiveUser(activeUserData);

        if (!activeUserData) {
          console.error("Active user not found in all users data.");
          return;
        }

        // Fetch compatibility matches for the active user
        const matchesResponse = await fetch(
          `http://localhost:5001/chattesting/${activeUserData.user_data_id}`,
          { signal: abortController.signal } // Pass the abort signal
        );
        const matchesData = await matchesResponse.json();
        console.log("Matches Data:", matchesData); // Log matches data

        if (matchesData.matches) {
          // Store compatibility data
          setDisplayedUsersChat(matchesData.matches);

          // Extract user IDs from the matches
          const userIds = matchesData.matches.map((match) => match.userID);
          console.log("User IDs from Matches:", userIds); // Log user IDs from matches

          // Find additional profile data for each matched user from the allUsersData
          const profiles = userIds.map((userId) =>
            allUsersData.find((user) => user.user_data_id === userId)
          );
          console.log("Profiles Data:", profiles); // Log profiles data
          setDisplayedUserProfile(profiles);

          // Set displayedUsers to the profiles
          setDisplayedUsers(profiles);
          console.log("Displayed Users Set:", profiles); // Log displayed users

          // Set the first profile as the initial displayed user
          setCurrentDisplayedUser(profiles[0]);
          console.log("Current Displayed User Set:", profiles[0]); // Log current displayed user
          setCurrentIndex(0);
        } else {
          console.error("No matches found in the response.");
        }
      } catch (error) {
        if (error.name !== "AbortError") {
          console.error("Error fetching data:", error);
        }
      }
    };

    fetchAllUsersData();

    // Cleanup function to abort the fetch request
    return () => {
      abortController.abort();
    };
  }, [activeUserId]); // Re-run effect when activeUserId changes

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