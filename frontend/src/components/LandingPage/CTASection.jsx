"use client";

/**
 * This is the call to action section of the landing page
 * It holds the large button to sign up with, and the two pieces of clickable text for login and continue as guest
 * All button functionality is used for redirecting to the pages labeled on the buttons
 */

import { useNavigate } from "react-router-dom";

const CTASection = () => {
  const navigate = useNavigate()

  const loginRedirect = () => {
    navigate('/Login');
  }

  const signupRedirect = () => {
    navigate('/Signup/step1')
  }

  return (
    <section className="flex flex-col gap-6 items-center">
      <button
        className=" text-2xl font-bold bg-teal-400 hover:bg-teal-300 cursor-pointer h-[70px] rounded-[1000px] 
                  text-neutral-900 w-[356px] max-md:text-2xl max-md:h-[60px] max-md:w-[300px] 
                    max-sm:w-full max-sm:text-xl max-sm:h-[50px] max-sm:max-w-[280px]"
        aria-label="Sign up for free"
        onClick={signupRedirect}
      >
        Sign up for Free
      </button>
      <div className="flex gap-2.5 items-center text-2xl font-bold text-white max-sm:flex-col max-sm:gap-4">

        <button 
          className="p-2.5 hover:underline cursor-pointer max-sm:text-xl"
          onClick={loginRedirect}
        >
          Log In
        </button>

        <div className="w-0.5 bg-white h-[45px] rotate-[30deg] max-sm:hidden" />

        <button className="p-2.5 hover:underline cursor-pointer max-sm:text-xl">
          Continue as Guest
        </button>

      </div>
    </section>
  );
};

export default CTASection;
