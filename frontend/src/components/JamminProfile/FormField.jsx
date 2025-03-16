import React from "react";

const FormField = ({ label, value }) => {
  return (
    <div className="flex items-center mb-3.5 max-sm:flex-col max-sm:gap-2.5 max-sm:items-start">
      <label className="text-2xl font-bold text-white w-[142px]">{label}</label>
      <div className="pl-4 text-2xl font-bold text-white rounded-md opacity-50 bg-stone-500 h-[49px] w-[315px] max-sm:w-full">
        {value}
      </div>
    </div>
  );
};

export default FormField;
