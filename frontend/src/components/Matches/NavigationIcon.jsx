"use client";
import React from "react";

const NavigationIcon = ({ svg, className = "" }) => {
  return (
    <div className={`flex justify-center p-2.5 ${className}`}>
      <div dangerouslySetInnerHTML={{ __html: svg }} />
    </div>
  );
};

export default NavigationIcon;
