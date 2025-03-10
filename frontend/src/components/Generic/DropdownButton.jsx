import React from "react";
import DropdownIcon from "./DropdownIcon";

const DropdownButton = ({ isOpen, onClick, itemSelectedText, variant="placeHolder" }) => {
  const variantStyles = {
    placeHolder: "text-stone-400",
    selected: "text-white",
  };

  return (
    <button
      id="dropdown-button"
      className="relative w-full rounded-md bg-stone-500 h-[59px] max-sm:h-[50px]"
      onClick={onClick}
      aria-expanded={isOpen}
      aria-haspopup="true"
      aria-controls="dropdown-menu"
    >
      <span className={`px-4 text-left block my-auto text-2xl font-bold ${variantStyles[variant]}`}>
        {itemSelectedText}
      </span>
      <DropdownIcon />
    </button>
  );
};

export default DropdownButton;
