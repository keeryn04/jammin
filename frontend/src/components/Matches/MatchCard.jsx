import React from "react";

const MatchCard = ({ image, name, age, genre }) => {
  return (
    <article className="flex items-center p-6 bg-black rounded">
      <img
        src={image}
        alt={`${name}'s profile`}
        className="w-[56px] h-[56px] rounded-[28px]"
      />
      <div className="flex-1 ml-4">
        <h3 className="text-base font-medium text-teal-400">
          {name}, {age}
        </h3>
        <p className="text-sm text-neutral-400">{genre}</p>
      </div>
      <div>
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-[24px] h-[24px]"
        >
          <g clipPath="url(#clip0_270_868)">
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M20.0306 9.53063L12.5306 17.0306C12.3899 17.1715 12.1991 17.2506 12 17.2506C11.8009 17.2506 11.6101 17.1715 11.4694 17.0306L3.96937 9.53063C3.67632 9.23757 3.67632 8.76243 3.96937 8.46937C4.26243 8.17632 4.73757 8.17632 5.03062 8.46937L12 15.4397L18.9694 8.46937C19.2624 8.17632 19.7376 8.17632 20.0306 8.46937C20.3237 8.76243 20.3237 9.23757 20.0306 9.53063V9.53063Z"
              fill="#34F7D0"
            />
          </g>
          <defs>
            <clipPath id="clip0_270_868">
              <rect width="24" height="24" fill="white" />
            </clipPath>
          </defs>
        </svg>
      </div>
    </article>
  );
};

export default MatchCard;
