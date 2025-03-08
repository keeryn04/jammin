"use client";

import Logo from "../Generic/Logo";
import Heading from "../Generic/Heading";
import CTASection from "./CTASection";

  const LandingPage = () => {
    return (
      <main className="fixed inset-0 flex flex-col h-screen w-screen overflow-hidden justify-center items-center bg-neutral-800">
        <header>
          <Logo />
        </header>
        <Heading text="Ready to meet new people to jam with?"/>
        <CTASection />
      </main>
    );
  };

export default LandingPage;
