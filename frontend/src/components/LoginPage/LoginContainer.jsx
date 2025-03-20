"use client";

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../Generic/Logo";
import Heading from "../Generic/Heading";
import FormInput from "../Generic/FormInput";
import ActionButton from "../Generic/ActionButton";

/**
 * This is the login container. It is the page displayed for the user such that they can input their email and password and login to the system
 * The components that make up this file are the logo svg, the form input, error message, and primary / secondary coloured buttons
 * The functions below contain functionality for handling clicking the buttons such as login and back, as well as functions that update the typed email and password
 * Login will check the email and password inputted against the database and either advance the user or display an error that either one is incorrect
 */

const VERCEL_URL = import.meta.env.VITE_VERCEL_URL;
const fetchLink = `${VERCEL_URL}/api/users`;
const loginLink = `${VERCEL_URL}/api/login`;
const redirectLink = `${VERCEL_URL}/api/spotify/login`;
const passwordLink = `${VERCEL_URL}/api/auth/password_check`

const LoginContainer = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const backendRedirect = async () => {
    try {
      window.location.href = redirectLink; 
    } catch (e) {
      console.error("Error:", e);
      setError("Error authenticating Spotify, please login and try again.");
    }
  };

  const attemptLogin = async (inputEmail, inputPassword) => {
    try {
      const response = await fetch(fetchLink);
      const data = await response.json();
      for (var i = 0; i < data.length; i++) {
        var user = data[i];        
        if (inputEmail === user["email"]){
          //Fetch savedPassword
          const response = await fetch(passwordLink, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ password: inputPassword })
        });
        
        const data = await response.json(); //{ match: true/false }
        const savedPassword = data.match;
        

          //Check if password entered was matched with database password
          if (savedPassword){
            //Save user_id as cookie via backend
            const loginReturn = await fetch(loginLink, {
              method: "POST",
              credentials: "include",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ user_id: user['user_id'] })
            });

            const data = await loginReturn.json();
            return true;
          }
        }
      }
      return false;
    } catch (error) {
      console.error("error fetching users / login attempt", error)
      return false
    }
  }

  const navigate = useNavigate()

  const handleLogin = async () => {
    //Check login information, then either advance the user, or display and error
    setEmail(email.toLowerCase());
    const loginSuccessful = await attemptLogin(email, password)
    if (loginSuccessful == true) {
      backendRedirect();
    }
    else {
      setError("Email or password incorrect")
    }
  };

  const handleEmailInput = (event) => {
    setEmail(event.target.value);
  }

  const handlePasswordInput = (event) => {
    setPassword(event.target.value);
  }

  const handleBack = () => {
    navigate("/");
  };

  return (
    <main className="fixed inset-0 flex flex-col h-screen w-screen overflow-hidden justify-center items-center bg-neutral-800">
      <Logo />

      <Heading text="Glad you have you back!" />

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
        {/*If error != null, error message will be displayed on screen*/}
        {error && (
          <p className="mx-0 my-5 text-2xl text-center text-red-500 max-sm:text-xl">
            {error}
          </p>
        )}

        <div className="flex mt-1.5 justify-center gap-4 items-center">
          <ActionButton variant="secondary" onClick={handleBack}>
            Back
          </ActionButton>

          <ActionButton variant="primary" onClick={handleLogin}>
            Log In
          </ActionButton>
        </div>
      </div>
    </main>
  );
};

export default LoginContainer;