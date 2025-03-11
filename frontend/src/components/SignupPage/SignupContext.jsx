"use client";

import React, { createContext, useContext, useState } from "react";

const SingupContext = createContext();

export const SignupProvider = ({ children }) => {
    const [signupData, setSignupData] = useState({
        email: "",
        password: ""
    });

    return (
        <SingupContext.Provider value={{ signupData, setSignupData}}>
            {children}
        </SingupContext.Provider>
    )
}

export const useSignupContext = () => useContext(SingupContext)