import React, { createContext, useState, useEffect } from "react";

// Create the context
export const UserContext = createContext();

// Create the provider component
export const UserProvider = ({ children }) => {
  const [activeUser, setActiveUser] = useState(null);
  const [displayedUsers, setDisplayedUsers] = useState([]);
  const [currentDisplayedUser, setCurrentDisplayedUser] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);

  // Fetch users from the database
  useEffect(() => {
    fetch("http://localhost:5000/api/user_data")
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          setActiveUser(data[0]); // Set the first user as activeUser
          setDisplayedUsers(data.slice(1)); // Set the remaining users as displayedUsers
          setCurrentDisplayedUser(data[1]); // Set the first user as the initial displayed user
          setCurrentIndex(0); // Initialize currentIndex to 0
        }
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);


  return (
    <UserContext.Provider
      value={{
        activeUser,
        displayedUsers,
        currentDisplayedUser,
        setCurrentDisplayedUser,
        currentIndex, // Provide currentIndex
        setCurrentIndex, // Provide setCurrentIndex
      }}
    >
      {children}
    </UserContext.Provider>
  );
};