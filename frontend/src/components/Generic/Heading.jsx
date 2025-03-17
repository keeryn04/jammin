/**
 * This is a formatted header used for the landing, login, and signup pages
 * Text is the text that will be displayed
 */

const Heading = ({text}) => {
    return (
      <h1 className="   mb-16 text-5xl 
                        font-bold text-center 
                        text-white sm:max-w-[866px] 
                      
                        sm:mb-20 
                        sm:text-7xl">
        {text}
      </h1>
    );
  };
  
  export default Heading;
  