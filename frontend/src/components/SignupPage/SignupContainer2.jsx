"use client";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../Generic/Logo";
import Heading from "../Generic/Heading";
import FormInput from "../Generic/FormInput";
import ActionButton from "../Generic/ActionButton";
import DropdownMenu from "../Generic/DropdownMenu"
import { useSignupContext } from "./SignupContext";

const SignupContainer2 = () => {
  const {signupData, setSignupData} = useSignupContext()
  const [name, setName] = useState("");
  const [gender, setGender] = useState("");
  const [age, setAge] = useState("")
  const [error, setError] = useState(null);

  const fetchLink = "http://localhost:5000/api/users";

  const attemptUserPost = async (signupData, name, gender, age) => {
    /*
    try {
      const response = await fetch(fetchLink, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: signupData['email'],
          password_hash: signupData['password'],
          username: name,
          age: age,
          gender: gender
        })
      });

      const data = await response.text();
      if (response.ok) {
        console.log("Signup Successful")
      } else {
        setError(data.error)
      }
      
    } catch (error) {
      console.error("error posting signup information", error)
      setError("Failed to signup, please try again")
    }*/
   console.error("NOT IMPLEMENTED YET, CHECK signupBranch FOR CURRENT CHANGES")
  }

  //Navigation
  const navigate = useNavigate()

  //Numeric checker for age
  const isNumeric = (value) => typeof value === "number" && !isNaN(value);

  const handleSignup = () => {
    //Input checking
    if (!isNumeric(age) || age <= 17 || age > 120)
      setError("Age must be a number between 18 and 120")
    else if (name.length > 40)
      setError("Name must be less than 40 characters long")
    else
      attemptUserPost(signupData, name, gender, age);
  };

  const handleBack = () => {
    navigate("/Signup/step1");
  };

  //Inputs
  const handleNameInput = (event) => {
    setName(event.target.value);
  }

  const handleAgeInput = (event) => {
    setAge(event.target.value);
  }

  const handleGenderInput = (value) => {
    setGender(value)
  }

  return (
    <main className="fixed inset-0 flex flex-col h-screen w-screen overflow-hidden justify-center items-center bg-neutral-800">
      <Logo />

      <Heading text="Just a bit more"/>

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

        <DropdownMenu 
          setValue = {handleGenderInput}
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
