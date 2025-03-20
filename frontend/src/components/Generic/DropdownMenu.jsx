"use client";
import React, { useState, useRef, useEffect } from "react";
import DropdownButton from "./DropdownButton";
import MenuItems from "./MenuItems";

const DropdownMenu = ( {setValue} ) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [selectedItem, setSelectedItem] = useState("Select your Gender...");
  const [variantStyle, setVariantStyle] = useState('placeHolder');
  const dropdownRef = useRef(null);

  const useClickOutside = (ref, handler) => {
    useEffect(() => {
      const listener = (event) => {
        if (!ref.current || ref.current.contains(event.target)) {
          return;
        }
        handler(event);
      };
  
      document.addEventListener("mousedown", listener);
      document.addEventListener("touchstart", listener);
  
      return () => {
        document.removeEventListener("mousedown", listener);
        document.removeEventListener("touchstart", listener);
      };
    }, [ref, handler]);
  };


  useClickOutside(dropdownRef, () => {
    setIsOpen(false);
    setActiveIndex(-1);
  });

  const handleToggle = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setActiveIndex(-1);
    }
  };

  const handleItemClick = (item) => {
    setVariantStyle("selected");
    setValue(item)
    setSelectedItem(item);
    setIsOpen(false);
    setActiveIndex(-1);
  };

  return (
  
      <div ref={dropdownRef} className="flex flex-col relative w-full text-left justify-center">
        <label className="mb-1 text-2xl font-bold text-white max-sm:text-xl">
          Gender
        </label>
        <DropdownButton
          isOpen={isOpen}
          onClick={handleToggle}
          itemSelectedText={selectedItem}
          variant={variantStyle}
        />
        <MenuItems
          isOpen={isOpen}
          activeIndex={activeIndex}
          onItemClick={handleItemClick}
        />
      </div>

  );
};

export default DropdownMenu;
