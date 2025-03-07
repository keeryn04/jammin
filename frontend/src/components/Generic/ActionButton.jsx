const ActionButton = ({ variant = "primary", onClick, children }) => {
    const baseStyles =
      "text-2xl font-bold cursor-pointer border-[none] h-[70px] rounded-[1000px] text-neutral-900 w-[170px] max-sm:w-full max-sm:text-xl max-sm:h-[60px]";
    const variantStyles = {
      primary: "bg-teal-400",
      secondary: "bg-neutral-400",
    };
  
    return (
      <button
        className={`${baseStyles} ${variantStyles[variant]}`}
        onClick={onClick}
      >
        {children}
      </button>
    );
  };
  
  export default ActionButton;
  