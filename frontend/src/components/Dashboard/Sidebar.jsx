import React from "react";
import {
  ExpandIcon,
  HomeIcon,
  ProfileIcon,
  UserIcon,
  SettingsIcon,
} from "./icons";

const NavItem = ({ children }) => (
  <button className="flex justify-center items-center mb-4 cursor-pointer h-[108px] w-[113px] max-md:h-[60px] max-md:w-[60px] max-sm:h-[50px] max-sm:w-[50px]">
    {children}
  </button>
);

export default function Sidebar() {
  return (
    <nav className="flex flex-col items-center px-0 py-5 bg-neutral-800 w-[152px] max-md:w-20 max-sm:w-[60px]">
      <div className="mb-10 h-[89px] w-[89px]">
        <ExpandIcon />
      </div>
      <NavItem>
        <HomeIcon />
      </NavItem>
      <NavItem>
        <ProfileIcon />
      </NavItem>
      <NavItem>
        <UserIcon />
      </NavItem>
      <NavItem>
        <SettingsIcon />
      </NavItem>
    </nav>
  );
}
