import React from "react";

const NavItem = ({ children }) => {
  return (
    <div className="flex justify-center items-center p-2.5 h-[108px] w-[113px] max-sm:h-[50px] max-sm:w-[50px]">
      <div>{children}</div>
    </div>
  );
};

export default NavItem;
