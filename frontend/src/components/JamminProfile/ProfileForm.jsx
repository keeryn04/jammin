import React, { useState, useEffect } from "react";

const UserProfileForm = () => {
  const userId = "2b77e1f5-fec0-11ef-85bd-0242ac120002"; // Hardcoded for testing
  const [formData, setFormData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/api/users/${userId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch user data");
        }
        return response.json();
      })
      .then((data) => {
        setFormData({
          username: data.username || "",
          email: data.email || "",
          password_hash: "",
          age: data.age || "",
          bio: data.bio || "",
          gender: data.gender || "",
          school: data.school || "",
          occupation: data.occupation || "",
          looking_for: data.looking_for || "",
          spotify_auth: data.spotify_auth || false,
        });
      })
      .catch((error) => {
        console.error("Error fetching user data:", error);
        setError("Could not load user data.");
      });
  }, []);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!formData) return <p className="text-white">Loading user data...</p>;

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`http://localhost:5000/api/users/${userId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to update profile");
        }
        return response.json();
      })
      .then(() => alert("Profile updated successfully!"))
      .catch((error) => {
        console.error("Error updating profile:", error);
        alert("Error updating profile. Please try again.");
      });
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 p-6 bg-neutral-900 rounded-lg shadow-md">
      <label className="text-white">
        Username:
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
          placeholder="Enter new password"
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
