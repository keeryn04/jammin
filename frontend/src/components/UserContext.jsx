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
  const activeUserId = "7d592cb4-04de-11f0-ba20-0242ac120002"; // Replace with your desired user_data_id

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

        // Fetch ALL matches from the matches endpoint
        const matchesResponse = await fetch(
          `http://localhost:5001/api/matches`,
          { signal: abortController.signal } // Pass the abort signal
        );
        const matchesData = await matchesResponse.json();
        console.log("All Matches Data:", matchesData); // Log all matches data

        // Filter out the active user from the list of all users
        const otherUsers = allUsersData.filter(
          (user) => user.user_data_id !== activeUserId
        );
        console.log("Other Users:", otherUsers); // Log other users

        // Call the LLM to generate compatibility data
        const llmResponse = await fetch(
          `http://localhost:5001/chattesting/${activeUserId}`,
          { signal: abortController.signal } // Pass the abort signal
        );
        const llmData = await llmResponse.json();
        console.log("LLM Response:", llmData); // Log the LLM response

        // Prepare the list of users to display
        const usersToDisplay = [];
        const compatibilityData = [];

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

              // Check if a match exists for this user
              const existingMatch = matchesData.find(
                (m) =>
                  m.user_1_id === activeUserId &&
                  m.user_2_id === user_id &&
                  m.status === "pending"
              );

              if (existingMatch) {
                // Update the match with LLM data
                await fetch(
                  `http://localhost:5001/api/matches/${existingMatch.match_id}`,
                  {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                      user_1_id: existingMatch.user_1_id,
                      user_2_id: existingMatch.user_2_id,
                      match_score: compatibility_score,
                      reasoning: reasoning,
                      status: "pending", // Keep status as pending
                    }),
                    signal: abortController.signal,
                  }
                );
                console.log("Updated match:", existingMatch.match_id);
              } else {
                // Create a new match with LLM data
                await fetch(`http://localhost:5001/api/matches`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    user_1_id: activeUserId,
                    user_2_id: user_id,
                    match_score: compatibility_score,
                    reasoning: reasoning,
                    status: "pending",
                  }),
                  signal: abortController.signal,
                });
                console.log("Created new match for user:", user_id);
              }
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
  }, [activeUserId]); // Re-run effect when activeUserId changes

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