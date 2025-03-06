const ProgressBar = ({ progress }) => {
    return (
      <div className="w-full h-2 rounded bg-neutral-600">
        <div
          className="h-full bg-green-500 rounded transition-all duration-300 hover:shadow-[0_0_8px_2px_rgba(74,222,128,0.8)]"
          style={{ width: `${progress}%` }}
        />
      </div>
    );
  };
  
  export default ProgressBar;