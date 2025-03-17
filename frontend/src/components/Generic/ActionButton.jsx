/**
 * This is a generic action button that can either be the primary teal colour, or a secondary grey colour
 * Pass the onClick function to it to install the functionality it needs for the program.
 * The children prop allows for defining the text that appears on it as well
 */

const ActionButton = ({ variant = "primary", onClick, children }) => {
    const baseStyles =
      "font-bold cursor-pointer border-[none] h-[60px] rounded-[1000px] text-neutral-900 sm:h-[70px]";
    const variantStyles = {
      primary: "text-xl sm:text-2xl bg-teal-400 hover:bg-teal-300 w-[130px] sm:w-[170px]",
      primaryLandingPage:  "text-xl sm:text-2xl bg-teal-400 hover:bg-teal-300 w-[270px] sm:w-[370px]",
      secondary: "text-xl sm:text-2xl bg-neutral-400 hover:bg-neutral-300 w-[130px] sm:w-[170px]",
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
  