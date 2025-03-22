import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../UserContext";

const MatchCard = ({ match_id, match_score, matched_at, reasoning, user_2_data_id }) => {
  const { allUsersData } = useContext(UserContext);
  const [matchedUser, setMatchedUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false); 

  const VERCEL_URL = import.meta.env.VITE_VERCEL_URL;

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // fetch user id from the users table using user_data_id
        const userIDResponse = await fetch(
          `${VERCEL_URL}/api/users/by_user_data/${user_2_data_id}`
        );

        if (!userIDResponse.ok) {
          throw new Error("Failed to fetch user info");
        }

        const userIDData = await userIDResponse.json(); 
        const userID = userIDData.user_id;  

        // fetch user data with the user_id
        const userResponse = await fetch(
          `${VERCEL_URL}/api/users/${userID}`
        );

        if (!userResponse.ok) {
          throw new Error("Failed to fetch user info");
        }

        const userDataArray = await userResponse.json();
        const userData = userDataArray[0];

        // find corresponding user_data entry in allUsersData
        const userDetails = allUsersData.find(
          (user) => user.user_data_id === user_2_data_id
        );

        if (!userDetails) {
          throw new Error("User data not found in allUsersData");
        }

        const combinedData = {
          ...userData,
          ...userDetails,
          image: userDetails.profile_image,
        };

        setMatchedUser(combinedData);
      } catch (error) {
        console.error("Error fetching user data:", error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [user_2_data_id, allUsersData]);

  if (loading) {
    return <div>Loading user data...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!matchedUser) {
    return <div>No user data found.</div>;
  }

  const { username, 
    age, 
    genre, 
    image, 
    gender, 
    looking_for, 
    occupation, 
    school, 
  } = matchedUser;

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <article className="flex flex-col p-6 bg-black rounded">
      <div className="flex items-center">
        <img
          src={image}
          alt={`${username}'s profile`}
          className="w-[56px] h-[56px] rounded-[28px]"
        />
        <div className="flex-1 ml-4">
          <h3 className="text-base font-medium text-teal-400">
            {username}, {age}
          </h3>
          <p className="text-sm text-neutral-400">{genre}</p>
          <p className="text-sm text-neutral-400">Match Score: {match_score}%</p>
          <p className="text-sm text-neutral-400">
            Matched on: {new Date(matched_at).toLocaleDateString()}
          </p>
        </div>
        <button onClick={toggleExpand} className="focus:outline-none">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`w-[24px] h-[24px] transform transition-transform ${
              isExpanded ? "rotate-180" : ""
            }`}
          >
            <g clipPath="url(#clip0_270_868)">
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M20.0306 9.53063L12.5306 17.0306C12.3899 17.1715 12.1991 17.2506 12 17.2506C11.8009 17.2506 11.6101 17.1715 11.4694 17.0306L3.96937 9.53063C3.67632 9.23757 3.67632 8.76243 3.96937 8.46937C4.26243 8.17632 4.73757 8.17632 5.03062 8.46937L12 15.4397L18.9694 8.46937C19.2624 8.17632 19.7376 8.17632 20.0306 8.46937C20.3237 8.76243 20.3237 9.23757 20.0306 9.53063V9.53063Z"
                fill="#34F7D0"
              />
            </g>
            <defs>
              <clipPath id="clip0_270_868">
                <rect width="24" height="24" fill="white" />
              </clipPath>
            </defs>
          </svg>
        </button>
      </div>
      {/* Expanded section */}
      {isExpanded && (
        <div className="space-y-4 m-5">
          {/* Reasoning Section */}
          <div className="p-4 bg-neutral-900 rounded-lg border border-neutral-700">
            <p className="text-base text-neutral-300 font-medium">{reasoning}</p>
          </div>
        
          {/* Profile Details Section */}
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-sm text-neutral-400">
              <p>{`Gender: ${gender ?? "Not specified"}`}</p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-neutral-400">
              <p>{`Looking For: ${looking_for ?? "Not specified"}`}</p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-neutral-400">
              <p>{`Occupation: ${occupation ?? "Not specified"}`}</p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-neutral-400">
              <p>{`School: ${school ?? "Not specified"}`}</p>
            </div>
          </div>
        </div>
      )}
    </article>
  );
};

export default MatchCard;