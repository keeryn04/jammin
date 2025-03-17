/**
 * This is a formatted header used for the landing, login, and signup pages
 * Text is the text that will be displayed
 */

const Heading = ({text}) => {
    return (
      <h1 className="   mb-5 text-4xl 
                        font-bold text-center 
                        text-white sm:max-w-[866px] 
                      
                        sm:mb-10 
                        sm:text-6xl">
        {text}
      </h1>
    );
  };
  
  export default Heading;
  