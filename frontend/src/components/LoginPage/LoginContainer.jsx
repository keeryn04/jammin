"use client";

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../Generic/Logo";
import Heading from "../Generic/Heading";
import FormInput from "../Generic/FormInput";
import ActionButton from "../Generic/ActionButton";

/**
 * This the login container. It is the page displayed for the user such that they can input their email and password and login to the system
 * The components that make up this file are the logo svg, the form input, error message, and primary / secondary coloured buttons
 * The functions below contain functionality for handling clicking the buttons such as login and back, as well as functions that update the typed email and password
 * Login will check the email and password inputted against the database and either advance the user or display an error that either one is incorrect
 */

const LoginContainer = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const fetchLink = "http://localhost:5000/api/users"
  const loginLink = "http://localhost:5000/api/login/"

  const attemptLogin = async (inputEmail, inputPassword) => {
    try {
      const response = await fetch(fetchLink);
      const data = await response.json();
      for (var i = 0; i < data.length; i++) {
        var user = data[i];
        if (inputEmail === user["email"] && inputPassword === user["password_hash"]){
          await fetch(loginLink, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: user["user_id"] }) //Send user_id to save it as session variable
          });
          return true;
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
    const loginSuccessful = await attemptLogin(email, password)
    if (loginSuccessful == true) {
      console.log("Woooooooooo")
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

        <div className="flex gap-10 justify-center max-sm:flex-col max-sm:gap-4 max-sm:items-center">
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
