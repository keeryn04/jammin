/**
 * This is a generic form input field for users to type into
 * It allows for either regular or hidden typing based on the type passed in the props (text or password)
 * it can also be given a label above it and the placeholder text inside of it for prompting the user
 * Finally it also gets a input handler that should be a react state setter so the value typed into it can be gathered for later use
 */

const FormInput = ({ label, type, placeholder, inputHandler }) => {
    return (
      <div className="mb-5 max-sm:mb-4 justify-items-start">
        <label className="mb-2 text-2xl font-bold text-white max-sm:text-xl">
          {label}
        </label>
        <div className="relative w-full rounded-md bg-stone-500 h-[59px] max-sm:h-[50px]">
          <input
            type={type}
            placeholder={placeholder}
            onChange={inputHandler}
            className="px-4 py-0 text-2xl font-bold placeholder-stone-400 text-white border-[none] size-full max-sm:text-xl"
          />
        </div>
      </div>
    );
  };
  
  export default FormInput;
  