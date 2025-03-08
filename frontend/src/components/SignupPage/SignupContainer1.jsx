"use client";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../Generic/Logo";
import Heading from "../Generic/Heading";
import FormInput from "../Generic/FormInput";
import ActionButton from "../Generic/ActionButton";

const SignupContainer1 = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordCheck, setPasswordCheck] = useState("")
  const [error, setError] = useState("Error Message Here");

  //Navigation
  const navigate = useNavigate()

  const handleNext = () => {
    navigate("/Signup2")
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
    <main className="fixed inset-0 flex flex-col h-screen w-screen overflow-hidden justify-center items-center bg-neutral-800">
      <Logo />

      <Heading text="Tell us about yourself!"/>
        
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
          <p className="mx-0 my-5 text-2xl text-center text-red-500 max-sm:text-xl">
            {error}
          </p>
        )}

        <div className="flex gap-10 justify-center max-sm:flex-col max-sm:gap-4 max-sm:items-center">
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
