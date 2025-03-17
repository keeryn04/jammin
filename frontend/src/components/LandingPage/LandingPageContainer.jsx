"use client";

/**
 * This is the container for the landing page of the system
 * This page prompts the user with a call to action to signup, login, or continue as a guest and navigates them to the respective page
 */

import Logo from "../Generic/Logo";
import Heading from "../Generic/Heading";
import CTASection from "./CTASection";

  const LandingPageContainer = () => {
    return (
      <main className="flex flex-col p-10 h-screen w-screen justify-center items-center bg-neutral-800">
        <header>
          <Logo />
        </header>
        <Heading text="Ready to meet new people to jam with?"/>
        <CTASection />
      </main>
    );
  };

export default LandingPageContainer;
