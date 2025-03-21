import React from "react";


export function NavItem({ icon, clickFunction}) {
    return (
        <button onClick = {clickFunction} className="group flex justify-center items-center cursor-pointer sm:h-[80%] sm:w-[80%] h-[8%] w-[8%]">
            <img className="hover:brightness-200" src={`${icon}`} />
        </button>
    );
}

export function LogOutNavItem({ logout_icon, red_logout_icon, clickFunction }) { 
    return (
        <button onClick = {clickFunction} className="group flex justify-center items-center cursor-pointer sm:h-[80%] sm:w-[80%] h-[20%] w-[20%]">
            <img className="group-hover:hidden" src={`${logout_icon}`} />
            <img className="hidden group-hover:block" src={`${red_logout_icon}`} />
        </button>
    );
}