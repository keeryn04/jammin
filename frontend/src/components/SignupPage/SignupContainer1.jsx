"use client";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../Generic/Logo";
import Heading from "../Generic/Heading";
import FormInput from "../Generic/FormInput";
import ActionButton from "../Generic/ActionButton";
import { useSignupContext } from "./SignupContext";

/**
 * This is the first cotainer for the signup process
 * This page includes prompts for the users email, password, and an additional entry of the password to confirm its what the user wanted to type
 * It then has a button for going back to the landing page, and a button for going to the next step of the process
 * There is error checking on the email that it doesn't already exist in the database (TO BE ADDED) and that both passwords entered match
 */

const VERCEL_URL = import.meta.env.VITE_VERCEL_URL_PREVIEW;
const fetchLink = `${VERCEL_URL}/api/users`

const SignupContainer1 = () => {
  const {signupData, setSignupData} = useSignupContext()
  const [email, setEmail] = useState(null);
  const [password, setPassword] = useState(null);
  const [passwordCheck, setPasswordCheck] = useState(null)
  const [error, setError] = useState(null);

  const checkEmailAlreadyExists = async (inputEmail) => {
    try {
      const response = await fetch(fetchLink);
      const data = await response.json();
      for (var i = 0; i < data.length; i++) {
        var user = data[i];
        if (inputEmail === user["email"]){
          return true;
        }
      }
      return false;
    } catch (error) {
      console.error("error fetching users / checking email attempt", error)
      return false
    }
  }

  //Navigation
  const navigate = useNavigate()

  //Email regex
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  const handleNext = async () => {
    const emailAlreadyExists = await checkEmailAlreadyExists(email);
    if (email === null || password === null || passwordCheck === null)
      setError("Please fill in all form inputs")
    else if (emailAlreadyExists) {
      setError("Email entered is already in use")
    }
    else if (!emailRegex.test(email))
      setError("Improper Email formating [___@___.___]")
    else if (password != passwordCheck) {
      setError("Passwords entered do not match")
    }
    else {
      //Clean the data going into the database since emails shouldn't be case sensitive
      setEmail(email.toLowerCase());
      setSignupData({...signupData, email, password})
      navigate("/Signup/step2")
    }
  };

  const handleBack = () => {
    navigate("/");
  };

  //Inputs
  const handleEmailInput = (event) => {
    setEmail(event.target.value);
  }

  const handlePasswordInput = (event) => {
    setPassword(event.target.value);
  }

  const handlePasswordCheckInput = (event) => {
    setPasswordCheck(event.target.value);
  }

  return (
    <main className="flex flex-col h-screen w-screen justify-center items-center bg-neutral-800
      overflow-y-auto [&::-webkit-scrollbar]:w-2
      [&::-webkit-scrollbar-track]:rounded-full
      [&::-webkit-scrollbar-track]:bg-gray-100
      [&::-webkit-scrollbar-thumb]:rounded-full
      [&::-webkit-scrollbar-thumb]:bg-gray-300
      dark:[&::-webkit-scrollbar-track]:bg-neutral-700
      dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500">
      <Logo />

      <Heading text="Please Create a Login"/>
        
      <div className="w-full max-w-[527px] max-md:max-w-[90%]">
        <FormInput 
          label="Email" 
          type="text" 
          placeholder="Enter your email..." 
          inputHandler={handleEmailInput}
        />

        <FormInput
          label="Password"
          type="password"
          placeholder="Enter your password..."
          inputHandler={handlePasswordInput}
        />

        <FormInput
          label="Re-enter Password"
          type="password"
          placeholder="Enter your password again..."
          inputHandler={handlePasswordCheckInput}
        />

        {error && (
          <p className="mx-0 text-lg text-center text-red-500">
            {error}
          </p>
        )}

        <div className="flex mt-1.5 justify-center gap-4 items-center">
          <ActionButton variant="secondary" onClick={handleBack}>
            Back
          </ActionButton>

          <ActionButton variant="primary" onClick={handleNext}>
            Next
          </ActionButton>
        </div>
      </div>
    </main>
  );
};

export default SignupContainer1;
