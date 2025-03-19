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
  const VERCEL_URL = import.meta.env.VITE_VERCEL_URL_PREVIEW;
  const cookieFetchLink = `${VERCEL_URL}/api/auth/check`;

  // Fetch all user data from users_music_data and initialize displayed users
  useEffect(() => {
    const abortController = new AbortController(); // Create an AbortController

    const fetchAllUsersData = async () => {
      try {
        // Fetch the active user ID
        const res = await fetch(cookieFetchLink, { credentials: "include" });
        const data = await res.json();
        const activeUserId = data.user.user_data_id

        if (!activeUserId) {
          console.error("No active user data_id found");
          return;
        }
        // Fetch all users from the users_music_data endpoint
        const allUsersDataResponse = await fetch(
          `${VERCEL_URL}/api/user_data`,
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

        // Fetch ALL matches from the matches endpoint
        const matchesResponse = await fetch(
          `${VERCEL_URL}/api/matches`,
          { signal: abortController.signal } // Pass the abort signal
        );
        const matchesData = await matchesResponse.json();
        console.log("All Matches Data:", matchesData); // Log all matches data

        // Filter out the active user from the list of all users
        const otherUsers = allUsersData.filter(
          (user) => user.user_data_id !== activeUserId
        );
        console.log("Other Users:", otherUsers); // Log other users

        // Prepare the list of users to display
        const usersToDisplay = [];
        const compatibilityData = [];

        // Call the LLM to generate compatibility data
        const llmResponse = await fetch(
          `${VERCEL_URL}/api/chattesting/${activeUserId}`,
          { signal: abortController.signal } // Pass the abort signal
        );
        const llmData = await llmResponse.json();
        console.log("LLM Response:", llmData); // Log the LLM response

        if (llmData.matches) {
          for (const match of llmData.matches) {
            const user_id = match.userID;
            const compatibility_score = match.compatibility_score;
            const reasoning = match.reasoning;

            // Find the user in the otherUsers list
            const user = otherUsers.find((u) => u.user_data_id === user_id);

            if (user) {
              // Add the user to the display list
              usersToDisplay.push(user);
              compatibilityData.push({
                userID: user_id,
                compatibility_score,
                reasoning,
              });
            }
          }
        }

        // Set the displayed users and compatibility data
        setDisplayedUsers(usersToDisplay);
        setDisplayedUsersChat(compatibilityData);
        setDisplayedUserProfile(usersToDisplay);

        // Set the first profile as the initial displayed user
        if (usersToDisplay.length > 0) {
          setCurrentDisplayedUser(usersToDisplay[0]);
          setCurrentIndex(0);
        } else {
          console.error("No users to display.");
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
  }, []); // Re-run effect when activeUserId changes

  return (
    <UserContext.Provider
      value={{
        activeUser,
        displayedUsers,
        displayedUsersChat, // Provide compatibility data
        displayedUserProfile, // Provide additional user profile data
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