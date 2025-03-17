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
      className="flex relative size-full items-center justify-left rounded-md bg-stone-500 h-[50px] sm:h-[59px]"
      onClick={onClick}
      aria-expanded={isOpen}
      aria-haspopup="true"
      aria-controls="dropdown-menu"
    >
      <span className={`flex px-4 py-0 justify-left items-center size-full text-xl sm:text-2xl font-bold ${variantStyles[variant]}`}>
        {itemSelectedText}
      </span>
      <DropdownIcon />
    </button>
  );
};

export default DropdownButton;
