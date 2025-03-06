"use client";

import Logo from "./Logo";
import Heading from "./Heading";
import CTASection from "./CTASection";

const LandingPage = () => {
  return (
    <main className="flex flex-col justify-center items-center min-h-100 bg-neutral-800">
      <header>
        <Logo />
      </header>
      <Heading />
      <CTASection />
    </main>
  );
};

export default LandingPage;
