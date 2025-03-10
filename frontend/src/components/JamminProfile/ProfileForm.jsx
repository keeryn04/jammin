import React from "react";
import FormField from "./FormField";

const ProfileForm = () => {
  const fields = [
    { label: "First Name", value: "John" },
    { label: "Last Name", value: "Doe" },
    { label: "Age", value: "69" },
    { label: "School", value: "Watson Elementary" },
    { label: "Occupation", value: "Beekeeper" },
    { label: "Looking For", value: "Fortnite duo" },
  ];

  return (
    <form>
      {fields.map((field, index) => (
        <FormField key={index} label={field.label} value={field.value} />
      ))}
    </form>
  );
};

export default ProfileForm;
