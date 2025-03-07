"use client";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../Generic/Logo";
import FormInput from "../Generic/FormInput";
import ActionButton from "../Generic/ActionButton";

const SignupContainer2 = () => {
  const [name, setName] = useState("");
  const [gender, setGender] = useState("");
  const [age, setAge] = useState("")
  const [error, setError] = useState("Error Message Here");


  //Navigation
  const navigate = useNavigate()

  const handleSignup = () => {
    navigate("/Profile")
  };

  const handleBack = () => {
    navigate("/Signup1");
  };

  //Inputs
  const handleNameInput = (event) => {
    setEmail(event.target.value);
  }

  const handleAgeInput = (event) => {
    setPassword(event.target.value);
  }


  return (
    <main className="fixed inset-0 flex flex-col h-screen w-screen overflow-hidden justify-center items-center bg-neutral-800">
      <Logo />

      <h1 className="mb-10 text-6xl font-bold text-center text-white max-md:text-5xl max-sm:text-4xl">
        Just a bit more
      </h1>

      <div className="w-full max-w-[527px] max-md:max-w-[90%]">
        <FormInput 
          label="Name" 
          type="text" 
          placeholder="Enter your name..." 
          inputHandler={handleNameInput}
        />


        <FormInput
          label="Age"
          type="text"
          placeholder="Enter your age..."
          inputHandler={handleAgeInput}
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

          <ActionButton variant="primary" onClick={handleSignup}>
            Sign Up
          </ActionButton>
        </div>
      </div>
    </main>
  );
};

export default SignupContainer2;
