/**
 * This is a generic action button that can either be the primary teal colour, or a secondary grey colour
 * Pass the onClick function to it to install the functionality it needs for the program.
 * The children prop allows for defining the text that appears on it as well
 */

const ActionButton = ({ variant = "primary", onClick, children }) => {
    const baseStyles =
      "text-2xl font-bold cursor-pointer border-[none] h-[70px] rounded-[1000px] text-neutral-900 w-[170px] sm:h-[60px]";
    const variantStyles = {
      primary: "bg-teal-400 hover:bg-teal-300",
      secondary: "bg-neutral-400 hover:bg-neutral-300",
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
  