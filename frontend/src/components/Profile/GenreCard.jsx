const GenreCard = ({ genre }) => {
    return (
      <article className="flex items-center p-4 rounded-lg border border-solid bg-neutral-800 border-neutral-600 h-[72px] w-[173px] max-sm:w-full group">
        <i className="ti ti-music mr-3 text-white" />
        <span className="text-base font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-300 to-green-500 group-hover:text-green-300 group-hover:drop-shadow-[0_0_8px_rgba(74,222,128,0.8)] transition-all duration-300">
          {genre}
        </span>
      </article>
    );
  };
  
  export default GenreCard;