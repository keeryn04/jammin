import React from "react";

const MenuItems = ({ isOpen, activeIndex, onItemClick }) => {
  const menuItems = ["Male", "Female", "Prefer Not to Specify"];

  return (
    <ul
      className={`absolute z-10 w-full left-0 top-full mt-1 bg-stone-500 rounded-md shadow-lg transition-all duration-200 ease-in-out ${
        isOpen
          ? "opacity-100 translate-y-0"
          : "opacity-0 -translate-y-2 pointer-events-none"
      }`}
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="dropdown-button"
    >
      {menuItems.map((item, index) => (
        <li key={item} role="none">
          <button
            className={`w-full text-left rounded-md px-4 py-3 text-2xl font-bold text-white hover:bg-stone-400 focus:bg-stone-300 focus:outline-none transition-colors ${
              activeIndex === index ? "bg-stone-300" : ""
            }`}
            role="menuitem"
            onClick={() => onItemClick(item)}
            tabIndex={isOpen ? 0 : -1}
          >
            {item}
          </button>
        </li>
      ))}
    </ul>
  );
};

export default MenuItems;
