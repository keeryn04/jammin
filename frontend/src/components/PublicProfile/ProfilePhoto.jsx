export const ProfilePhoto = () => {
    return (
      <section className="flex flex-col gap-5">
        <h2 className="text-2xl font-bold text-left text-white max-sm:text-xl">
          Profile Photo
        </h2>
        <div
          dangerouslySetInnerHTML={{
            __html:
              '<svg id="21:111" layer-name="Flattened Logo " width="65" height="65" viewBox="0 0 65 65" fill="none" xmlns="http://www.w3.org/2000/svg" class="profile-photo" style="width: 65px; height: 65px"> <path d="M65 32.5C65 50.4493 50.4493 65 32.5 65C14.5507 65 0 50.4493 0 32.5C0 14.5507 14.5507 0 32.5 0C50.4493 0 65 14.5507 65 32.5Z" fill="#1ED7B2"></path> <path d="M17.5676 22.2789H17.5775L17.5676 22.2626V22.2789Z" fill="#151515"></path> <path d="M26.3426 47.1257C25.7259 45.4562 25.8552 42.7737 28.4344 40.0205L22.6448 30.5595L20.662 32.6661C15.5943 38.0506 14.1287 44.9412 16.3053 50.8334C18.4938 56.7581 24.1073 60.87 31.2224 60.9273C36.1349 60.967 40.3717 59.0757 43.331 55.8027C46.2286 52.598 47.6354 48.3754 47.6354 44.0786V22.2789H55.3613L48.8134 11.5786H17.77L24.318 22.2789H36.9351V44.0786C36.9351 46.0902 36.2816 47.6448 35.3941 48.6263C34.5684 49.5395 33.2953 50.2435 31.3087 50.2274C28.5222 50.205 26.9489 48.7671 26.3426 47.1257Z" fill="#151515"></path> </svg>',
          }}
        />
      </section>
    );
  };
  