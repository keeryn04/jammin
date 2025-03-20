"use client";

/**
 * This is the call to action section of the landing page
 * It holds the large button to sign up with, and the two pieces of clickable text for login and continue as guest
 * All button functionality is used for redirecting to the pages labeled on the buttons
 */

import { useNavigate } from "react-router-dom";
import ActionButton from "../Generic/ActionButton";

const CTASection = () => {
  const navigate = useNavigate()

  const loginRedirect = () => {
    navigate('/Login');
  }

  const signupRedirect = () => {
    navigate('/Signup/step1')
  }

  return (
    <section className="flex flex-col items-center my-2">
      <ActionButton onClick={signupRedirect} variant="primaryLandingPage">Sign up for Free</ActionButton>
      <div className="flex items-center text-2xl font-bold text-white sm:flex-row gap-1">

        <button 
          className="my-2 hover:underline cursor-pointer max-sm:text-xl"
          onClick={loginRedirect}
        >
          Log In
        </button>
      </div>
    </section>
  );
};

export default CTASection;
