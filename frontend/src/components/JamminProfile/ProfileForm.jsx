import React, { useState, useEffect } from "react";

const VERCEL_URL = import.meta.env.VITE_VERCEL_URL;
const usersLink = `http://localhost:5001/api/users`;
const userDataToUserLink = `http://localhost:5001/api/users/by_user_data`;

const UserProfileForm = ({ activeUser }) => {
  const [formData, setFormData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Step 1: Fetch all users
        const usersResponse = await fetch(usersLink);
        if (!usersResponse.ok) {
          throw new Error("Failed to fetch users");
        }
        const users = await usersResponse.json();

        // Step 2: Find the user with the matching user_data_id
        const activeUserData = users.find(
          (user) => user.user_data_id === activeUser.user_data_id
        );

        if (!activeUserData) {
          throw new Error("Active user not found in the users list");
        }

        // Step 3: Set form data
        setFormData({
          username: activeUserData.username || "",
          email: activeUserData.email || "",
          password_hash: activeUserData.password_hash || "",
          age: activeUserData.age || "",
          bio: activeUserData.bio || "",
          gender: activeUserData.gender || "",
          school: activeUserData.school || "",
          occupation: activeUserData.occupation || "",
          looking_for: activeUserData.looking_for || "",
          spotify_auth: activeUserData.spotify_auth || false,
        });
      } catch (error) {
        console.error("Error fetching user data:", error);
        setError("Could not load user data.");
      }
    };

    fetchUserData();
  }, [activeUser.user_data_id]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!formData) return <p className="text-white">Loading user data...</p>;

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Fetch the user ID based on user_data_id
      const response = await fetch(`${userDataToUserLink}/${activeUser.user_data_id}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error fetching user data:', response.status, errorText);
        return; // Exit the function early if the fetch fails
      }

      // Parse the JSON response
      const data = await response.json();
      console.log('User data:', data);

      const userId = data.user_id;
      console.log('User ID:', userId);

      // Filter out empty fields from formData
      const updatedData = Object.keys(formData).reduce((acc, key) => {
        if (key === "password_hash") {
          // Only include password_hash if it's not empty
          if (formData[key] !== "") {
            acc[key] = formData[key];
          } else {
            // Explicitly set password_hash to null if it's empty
            acc[key] = null;
          }
        } else {
          // Include other fields if they are not empty
          if (formData[key] !== "" && formData[key] !== null && formData[key] !== undefined) {
            acc[key] = formData[key];
          }
        }
        return acc;
      }, {});

      console.log('Updated Data:', updatedData);

      // Send the PUT request with only non-empty fields
      const updateResponse = await fetch(`${usersLink}/${userId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedData),
      });

      if (!updateResponse.ok) {
        throw new Error("Failed to update profile");
      }

      alert("Profile updated successfully!");
    } catch (error) {
      console.error("Error updating profile:", error);
      alert("Error updating profile. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 p-6 bg-neutral-900 rounded-lg shadow-md">
      <label className="text-white">
        Full Name:
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Email:
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Password:
        <input
          type="password"
          name="password_hash"
          placeholder="Enter new password (leave empty to not change)"
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Age:
        <input
          type="number"
          name="age"
          value={formData.age}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Bio:
        <textarea
          name="bio"
          value={formData.bio}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Gender:
        <input
          type="text"
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        School:
        <input
          type="text"
          name="school"
          value={formData.school}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Occupation:
        <input
          type="text"
          name="occupation"
          value={formData.occupation}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Looking For:
        <input
          type="text"
          name="looking_for"
          value={formData.looking_for}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <button
        type="submit"
        className="bg-teal-500 text-white p-2 rounded-md hover:bg-teal-600 transition-all"
      >
        Save Changes
      </button>
    </form>
  );
};

export default UserProfileForm;