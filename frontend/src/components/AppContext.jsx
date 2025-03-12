"use client";

import React, { createContext, useContext, useState } from "react";

const GlobalContext = createContext();

export const GlobalDataProvider = ({ children }) => {
    const [globalData, setGlobalData] = useState({
        loggedInUserID: ""
    });

    return (
        <GlobalContext.Provider value={{ globalData, setGlobalData }}>
            {children}
        </GlobalContext.Provider>
    )
}

export const useGlobalContext = () => useContext(GlobalContext)