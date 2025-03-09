import React from "react";
import {
  MatchesIcon,
  MatchesIconHover,
  HomeIcon,
  HomeIconHover,
  ProfileIcon,
  ProfileIconHover,
  UserIcon,
  UserIconHover,
  SettingsIcon,
  SettingsIconHover,
} from "./icons";

const NavItem = ({ DefaultIcon, HoverIcon }) => (
  <button className="group flex justify-center items-center cursor-pointer h-[108px] w-[113px] max-md:h-[60px] max-md:w-[60px] max-sm:h-[50px] max-sm:w-[50px]">
    <div className="w-25 h-25 max-md:w-10 max-md:h-10 max-sm:w-8 max-sm:h-8 flex justify-center items-center transition-all duration-300">
      {/* Default Icon (shown normally) */}
      <div className="block group-hover:hidden">
        <DefaultIcon />
      </div>

      {/* Hover Icon (shown on hover) */}
      <div className="hidden group-hover:block">
        <HoverIcon />
      </div>
    </div>
  </button>
);


export default function NavigationBar() {
  return (
    <nav className="flex flex-col items-center px-0 py-5 bg-neutral-800 w-[152px] max-md:w-20 max-sm:w-[60px] h-full justify-between">
      <div className="flex flex-col flex-1 justify-evenly items-center w-full">
        <NavItem DefaultIcon={MatchesIcon} HoverIcon={MatchesIconHover} />
        <NavItem DefaultIcon={HomeIcon} HoverIcon={HomeIconHover} />
        <NavItem DefaultIcon={ProfileIcon} HoverIcon={ProfileIconHover} />
        <NavItem DefaultIcon={UserIcon} HoverIcon={UserIconHover} />
        <NavItem DefaultIcon={SettingsIcon} HoverIcon={SettingsIconHover} />
      </div>
    </nav>
  );
}

