import React, { useState, useEffect } from "react";

const VERCEL_URL = import.meta.env.VITE_VERCEL_URL;
const usersLink = `http://localhost:5001/api/users`;
const userDataToUserLink = `http://localhost:5001/api/users/by_user_data`;

const UserProfileForm = ({ activeUser }) => {
  const [formData, setFormData] = useState(null);
  const [error, setError] = useState(null);
  const [validationErrors, setValidationErrors] = useState({});

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const usersResponse = await fetch(usersLink);
        if (!usersResponse.ok) {
          throw new Error("Failed to fetch users");
        }
        const users = await usersResponse.json();

        const activeUserData = users.find(
          (user) => user.user_data_id === activeUser.user_data_id
        );

        if (!activeUserData) {
          throw new Error("Active user not found in the users list");
        }

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
          contact: activeUserData.contact || "",
          spotify_auth: activeUserData.spotify_auth || false,
        });
      } catch (error) {
        console.error("Error fetching user data:", error);
        setError("Could not load user data.");
      }
    };

    fetchUserData();
  }, [activeUser.user_data_id]);

  const validateForm = () => {
    const errors = {};

    if (formData.age < 13) {
      errors.age = "Age must be at least 13.";
    }

    if (formData.bio.length > 50) {
      errors.bio = "Bio must be 50 characters or less.";
    }

    if (formData.school.length > 30) {
      errors.school = "School must be 30 characters or less.";
    }

    if (formData.occupation.length > 30) {
      errors.occupation = "Occupation must be 30 characters or less.";
    }

    if (formData.looking_for.length > 30) {
      errors.looking_for = "Looking for must be 30 characters or less.";
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = "Invalid email format.";
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      const response = await fetch(`${userDataToUserLink}/${activeUser.user_data_id}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error fetching user data:', response.status, errorText);
        return;
      }

      const data = await response.json();
      const userId = data.user_id;

      const updatedData = Object.keys(formData).reduce((acc, key) => {
        if (key === "password_hash") {
          if (formData[key] !== "") {
            acc[key] = formData[key];
          } else {
            acc[key] = null;
          }
        } else {
          if (formData[key] !== "" && formData[key] !== null && formData[key] !== undefined) {
            acc[key] = formData[key];
          }
        }
        return acc;
      }, {});

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

  if (error) return <p className="text-red-500">{error}</p>;
  if (!formData) return <p className="text-white">Loading user data...</p>;

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
        {validationErrors.email && <p className="text-red-500">{validationErrors.email}</p>}
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
          min="13"
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
        {validationErrors.age && <p className="text-red-500">{validationErrors.age}</p>}
      </label>

      <label className="text-white">
        Bio:
        <textarea
          name="bio"
          value={formData.bio}
          onChange={handleChange}
          maxLength="50"
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
        {validationErrors.bio && <p className="text-red-500">{validationErrors.bio}</p>}
      </label>

      <label className="text-white">
        Gender:
        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        >
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
          maxLength="30"
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
        {validationErrors.school && <p className="text-red-500">{validationErrors.school}</p>}
      </label>

      <label className="text-white">
        Occupation:
        <input
          type="text"
          name="occupation"
          value={formData.occupation}
          onChange={handleChange}
          maxLength="30"
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
        {validationErrors.occupation && <p className="text-red-500">{validationErrors.occupation}</p>}
      </label>

      <label className="text-white">
        Looking For:
        <input
          type="text"
          name="looking_for"
          value={formData.looking_for}
          onChange={handleChange}
          maxLength="30"
          className="p-2 w-full rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
        />
        {validationErrors.looking_for && <p className="text-red-500">{validationErrors.looking_for}</p>}
      </label>

      <label className="text-white">
        Contact:
        <input
          type="text"
          name="contact"
          value={formData.contact}
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