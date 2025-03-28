import React, { useState, useEffect } from "react";

const VERCEL_URL = import.meta.env.VITE_VERCEL_URL;
const usersLink = `${VERCEL_URL}/api/users`;
const userDataToUserLink = `${VERCEL_URL}/api/users/by_user_data`;
const hashPasswordLink = `${VERCEL_URL}/api/auth/hash_password`;

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
      // Fetch user ID based on user_data_id
      const response = await fetch(`${userDataToUserLink}/${activeUser.user_data_id}`);
  
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Error fetching user data:", response.status, errorText);
        setError("Failed to fetch user data. Please try again.");
        return;
      }
  
      const data = await response.json();
      const userId = data.user_id;
  
      // Create a copy of formData to avoid mutating the state directly
      let updatedData = { ...formData };
  
      {/*
      // Hash the password only if it is provided (not empty)
      if (formData.password_hash && formData.password_hash.trim() !== "") {
        const hashResponse = await fetch(hashPasswordLink, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ password: formData.password_hash }),
        });
  
        if (!hashResponse.ok) {
          const hashErrorText = await hashResponse.text();
          console.error("Error hashing password:", hashResponse.status, hashErrorText);
          throw new Error("Failed to hash password");
        }
  
        const hashData = await hashResponse.json();
        updatedData.password_hash = hashData.hashed_password; // Update with hashed password
      } else {
        // If the password field is empty, retain the existing password_hash
        // Do not include password_hash in updatedData to avoid updating it
        delete updatedData.password_hash;
      }
      */}
  
      // Filter out empty fields (optional, but recommended)
      updatedData = Object.fromEntries(
        Object.entries(updatedData).filter(
          ([_, value]) => value !== "" && value !== null && value !== undefined
        )
      );
  
      // Send the PUT request with only non-empty fields
      const updateResponse = await fetch(`${usersLink}/${userId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedData),
      });
  
      if (!updateResponse.ok) {
        const updateErrorText = await updateResponse.text();
        console.error("Error updating profile:", updateResponse.status, updateErrorText);
        throw new Error("Failed to update profile");
      }
  
      alert("Profile updated successfully!");
    } catch (error) {
      console.error("Error updating profile:", error);
      setError("Error updating profile. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 p-6 bg-neutral-900 rounded-lg shadow-md">
      <label className="text-white">
        Full Name:
        <input
          type="text"
          name="username"
          maxLength="30"
          value={formData.username}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      {/*<label className="text-white">
        Email:
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>
        {validationErrors.email && <p className="text-red-500">
        {validationErrors.email}</p>}
      </label>*/}

      {/*
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
      */}

      <label className="text-white">
        Age:
        <input
          type="number"
          name="age"
          value={formData.age}
          min="18"
          max="120"
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Bio:
        <input
          name="bio"
          value={formData.bio}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
      </label>

      <label className="text-white">
        Gender:
        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400">
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
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