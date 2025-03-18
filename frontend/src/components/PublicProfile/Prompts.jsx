import React, { useState } from "react";

const PromptBubble = ({ text, onClick }) => (
  <p
    className="px-3 py-1.5 text-lg tracking-tight leading-6 bg-gray-200 rounded-2xl text-stone-400 max-sm:text-base cursor-pointer"
    onClick={onClick}
  >
    {text}
  </p>
);

export const Prompts = () => {
  const [message, setMessage] = useState(null);

  const prompts = [
    "Desert island song...?",
    "Theme song to my life...",
    "Best road trip album...?",
  ];

  const handleClick = () => {
    setMessage("Coming Soon!");
    setTimeout(() => setMessage(null), 2000); // Hide the message after 2 seconds
  };

  return (
    <section className="flex flex-col gap-5">
      <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
        Prompts
      </h2>
      <div className="flex flex-col gap-5">
        {prompts.map((prompt, index) => (
          <PromptBubble key={index} text={prompt} onClick={handleClick} />
        ))}
      </div>

      {/* Small, unintrusive pop-up message */}
      {message && (
        <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-neutral-700 text-white px-4 py-2 rounded-lg shadow-lg text-sm">
          {message}
        </div>
      )}
    </section>
  );
};