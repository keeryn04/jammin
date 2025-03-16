import React from "react";

const NavItem = ({ DefaultIcon }) => (
  <button className="group flex justify-center items-center cursor-pointer lg:h-[100%] lg:w-[100%] md:h-[90%] md:w-[90%] sm:h-[80%] sm:w-[80%] ">
    <img className="hover:brightness-200" src={`${DefaultIcon}`} />
  </button>
);


export default function Navbar() {
  return (
    <nav className="flex flex-col lg:w-[80%] md:w-[70%] sm:w-[60%] items-center bg-neutral-800 rounded-full h-2/3 m-4">
      <div className="flex flex-col flex-1 justify-evenly items-center">
        <NavItem DefaultIcon={"/icons/MatchesIcon.png"} />
        <NavItem DefaultIcon={"/icons/ProfileIcon.png"} />
        <NavItem DefaultIcon={"/icons/AIIcon.png"} />
        <NavItem DefaultIcon={"/icons/SettingsIcon.png"} />
        <NavItem DefaultIcon={"/icons/InfoIcon.png"} />
      </div>
    </nav>
  );
}

