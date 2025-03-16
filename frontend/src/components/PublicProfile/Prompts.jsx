const PromptBubble = ({ text }) => (
    <p className="px-3 py-1.5 text-lg tracking-tight leading-6 bg-gray-200 rounded-2xl text-stone-400 max-sm:text-base">
      {text}
    </p>
  );
  
  export const Prompts = () => {
    const prompts = [
      "Desert island song...?",
      "Theme song to my life...",
      "Best road trip album...?",
    ];
  
    return (
      <section className="flex flex-col gap-5">
        <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
          Prompts
        </h2>
        <div className="flex flex-col gap-5">
          {prompts.map((prompt, index) => (
            <PromptBubble key={index} text={prompt} />
          ))}
        </div>
      </section>
    );
  };
  