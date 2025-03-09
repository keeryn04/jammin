const ArtistItem = ({ image, name }) => {
    return (
      <article className="flex gap-2.5 items-center">
        <img src={image} alt={name} className="object-cover w-12 h-12" />
        <h3 className="text-base font-medium tracking-tight leading-7 text-white max-sm:text-sm">
          {name}
        </h3>
      </article>
    );
  };
  
  export const TopArtists = () => {
    const artists = [
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/a905c04f885cc27681e8033aa2928b7d6de2eae8",
        name: "Troye Sivan",
      },
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/8d289db1625bedb6921aff8a0a014bcb33363992",
        name: "mehro",
      },
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/a905c04f885cc27681e8033aa2928b7d6de2eae8",
        name: "Troye Sivan",
      },
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/8d289db1625bedb6921aff8a0a014bcb33363992",
        name: "mehro",
      },
      {
        image:
          "https://cdn.builder.io/api/v1/image/assets/TEMP/a905c04f885cc27681e8033aa2928b7d6de2eae8",
        name: "mehro",
      },
    ];
  
    return (
      <section className="flex flex-col gap-5 padding-">
        <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
          Top 5 Artists
        </h2>
        <div className="flex flex-col gap-5">
          {artists.map((artist, index) => (
            <ArtistItem key={index} {...artist} />
          ))}
        </div>
        <div className="h-1"></div> {/* Adds spacing below TopArtists */}
      </section>
    );
  };
  