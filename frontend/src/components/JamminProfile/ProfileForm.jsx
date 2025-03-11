import React from "react";

const ProfileForm = () => {
  const fields = [
    { label: "First Name", value: "John" },
    { label: "Last Name", value: "Doe" },
    { label: "Age", value: "69" },
    { label: "School", value: "Watson Elementary" },
    { label: "Occupation", value: "Beekeeper" },
    { label: "Looking For", value: "Fortnite duo" },
    { label: "Social Media Link", value: "instabook.com" },
  ];

  return (
    <form className="flex flex-col gap-4 pb-6">
      {fields.map((field, index) => (
        <div key={index} className="flex flex-col">
          <label className="text-white text-sm font-semibold mb-1">{field.label}</label>
          <input
            type="text"
            placeholder={field.value}
            className="p-2 rounded-md bg-neutral-700 text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
          />
        </div>
      ))}
    </form>
  );
};

export default ProfileForm;
