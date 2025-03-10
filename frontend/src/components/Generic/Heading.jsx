/**
 * This is a formatted header used for the landing, login, and signup pages
 * Text is the text that will be displayed
 */

const Heading = ({text}) => {
    return (
      <h1 className="   mb-16 text-6xl 
                        font-bold text-center 
                        text-white max-w-[866px] 
                        max-md:text-5xl max-md:max-w-[700px] 
                        max-sm:mb-20 
                        max-sm:max-w-full 
                        max-sm:text-4xl">
        {text}
      </h1>
    );
  };
  
  export default Heading;
  