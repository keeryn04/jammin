const TrackItem = ({ image, name, artist }) => {
    return (
      <article className="flex gap-2.5 items-center">
        <img
          src={image}
          alt={`${name} by ${artist}`}
          className="object-cover w-12 h-12"
        />
        <div className="flex flex-col">
          <h3 className="text-base font-medium tracking-tight leading-7 text-white max-sm:text-sm">
            {name}
          </h3>
          <p className="text-sm font-medium text-zinc-400 max-sm:text-xs">
            {artist}
          </p>
        </div>
      </article>
    );
  };
  
  export const TopTracks = () => {
    const tracks = [
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/a905c04f885cc27681e8033aa2928b7d6de2eae8",
        name: "Easy",
        artist: "Troye Sivan",
      },
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/8d289db1625bedb6921aff8a0a014bcb33363992",
        name: "chance with you",
        artist: "mehro",
      },
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/a905c04f885cc27681e8033aa2928b7d6de2eae8",
        name: "Easy",
        artist: "Troye Sivan",
      },
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/8d289db1625bedb6921aff8a0a014bcb33363992",
        name: "chance with you",
        artist: "mehro",
      },
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/a905c04f885cc27681e8033aa2928b7d6de2eae8",
        name: "Easy",
        artist: "Troye Sivan",
      },
    ];
  
    return (
      <section className="flex flex-col gap-5">
        <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
          Top 5 Tracks
        </h2>
        <div className="flex flex-col gap-5">
          {tracks.map((track, index) => (
            <TrackItem key={index} {...track} />
          ))}
        </div>
      </section>
    );
  };
  