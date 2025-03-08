"use client";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../Generic/Logo";
import FormInput from "../Generic/FormInput";
import ActionButton from "../Generic/ActionButton";

const LoginContainer = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const navigate = useNavigate()

  const handleLogin = () => {
    //Check login information, then either advance the user, or display and error
    if (false /* Change to database check */) {
      //Add pathing
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

      <h1 className="mb-10 text-6xl font-bold text-center text-white max-md:text-5xl max-sm:text-4xl">
        Glad you have you back!
      </h1>

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
