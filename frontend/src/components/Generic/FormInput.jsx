/**
 * This is a generic form input field for users to type into
 * It allows for either regular or hidden typing based on the type passed in the props (text or password)
 * it can also be given a label above it and the placeholder text inside of it for prompting the user
 * Finally it also gets a input handler that should be a react state setter so the value typed into it can be gathered for later use
 */

const FormInput = ({ label, type, placeholder, inputHandler }) => {
    return (
      <div className="mb-4 sm:mb-5 justify-items-start">
        <label className="mb-2 text-xl font-bold text-white sm:text-2xl">
          {label}
        </label>
        <div className="relative w-full rounded-md bg-stone-500 h-[50px] sm:h-[59px]">
          <input
            type={type}
            placeholder={placeholder}
            onChange={inputHandler}
            className="px-4 py-0 text-xl font-bold placeholder-stone-400 text-white border-[none] size-full sm:text-2xl"
          />
        </div>
      </div>
    );
  };
  
  export default FormInput;
  