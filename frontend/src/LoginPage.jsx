import React from 'react';
import { Link } from 'react-router-dom';

function LoginPage() {
  return (
    <div>
      <h1>The Lorax</h1>
      <Link to="/Home">
        <button className="btn">Back</button>
      </Link>

      <div
        className="relative flex size-full min-h-screen flex-col bg-[#122117] dark group/design-root overflow-x-hidden"
        style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}
      >
        <div className="flex items-center bg-[#122117] p-4 pb-2 justify-end">
          <div className="flex w-12 items-center justify-end">
            <button className="flex max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-12 bg-transparent text-white gap-2 text-base font-bold leading-normal tracking-[0.015em] min-w-0 p-0">
              <div className="text-white" data-icon="Share" data-size="24px" data-weight="regular">
                <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                  <path d="M229.66,109.66l-48,48a8,8,0,0,1-11.32-11.32L204.69,112H165a88,88,0,0,0-85.23,66,8,8,0,0,1-15.5-4A103.94,103.94,0,0,1,165,96h39.71L170.34,61.66a8,8,0,0,1,11.32-11.32l48,48A8,8,0,0,1,229.66,109.66ZM192,208H40V88a8,8,0,0,0-16,0V208a16,16,0,0,0,16,16H192a8,8,0,0,0,0-16Z"></path>
                </svg>
              </div>
            </button>
          </div>
        </div>
        <div className="flex p-4 @container">
          <div className="flex w-full flex-col gap-4 items-center">
            <div className="flex gap-4 flex-col items-center">
              <div
                className="bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-xl min-h-32 w-32"
                style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/02f006a2-3c00-45dd-bf79-a23449fc75d8.png")' }}
              ></div>
              <div className="flex flex-col items-center justify-center">
                <p className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] text-center">Ariel, 28</p>
                <p className="text-[#95c6a6] text-base font-normal leading-normal text-center">Los Angeles, CA</p>
              </div>
            </div>
          </div>
        </div>
        <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">You and Ariel</h2>
        <div className="flex flex-col gap-3 p-4">
          <div className="flex gap-6 justify-between">
            <p className="text-white text-base font-medium leading-normal">Compatibility Score</p>
            <p className="text-white text-sm font-normal leading-normal">85%</p>
          </div>
          <div className="rounded bg-[#366346]">
            <div className="h-2 rounded bg-[#1dd75e]" style={{ width: '85%' }}></div>
          </div>
        </div>
        <div className="flex items-center gap-4 bg-[#122117] px-4 min-h-14 justify-between">
          <p className="text-white text-base font-normal leading-normal flex-1 truncate">Common Top Songs</p>
          <div className="shrink-0">
            <div className="text-white flex size-7 items-center justify-center" data-icon="ArrowRight" data-size="24px" data-weight="regular">
              <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                <path d="M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z"></path>
              </svg>
            </div>
          </div>
        </div>
        <div className="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-4">
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 flex-col">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg w-10 shrink-0"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/3aafafa5-f6ab-40db-94c3-df400410ca50.png")' }}
            ></div>
            <div className="flex flex-col gap-1">
              <h2 className="text-white text-base font-bold leading-tight">Coldplay</h2>
              <p className="text-[#95c6a6] text-sm font-normal leading-normal">My Universe</p>
            </div>
          </div>
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 flex-col">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg w-10 shrink-0"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/31a6c44b-af13-476a-8aea-f5496c23e288.png")' }}
            ></div>
            <div className="flex flex-col gap-1">
              <h2 className="text-white text-base font-bold leading-tight">TOPloader</h2>
              <p className="text-[#95c6a6] text-sm font-normal leading-normal">Dancing in the Moonlight</p>
            </div>
          </div>
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 flex-col">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg w-10 shrink-0"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/4b59ef04-91e6-4e16-b75d-01b936d551a3.png")' }}
            ></div>
            <div className="flex flex-col gap-1">
              <h2 className="text-white text-base font-bold leading-tight">Peach Tree Rascals</h2>
              <p className="text-[#95c6a6] text-sm font-normal leading-normal">Seventeen</p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-4 bg-[#122117] px-4 min-h-14 justify-between">
          <p className="text-white text-base font-normal leading-normal flex-1 truncate">Common Top Albums</p>
          <div className="shrink-0">
            <div className="text-white flex size-7 items-center justify-center" data-icon="ArrowRight" data-size="24px" data-weight="regular">
              <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                <path d="M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z"></path>
              </svg>
            </div>
          </div>
        </div>
        <div className="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-4">
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 items-center">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg w-10 shrink-0"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/6cb79d2b-3b39-4e08-b73b-ebea8f1d2b27.png")' }}
            ></div>
            <h2 className="text-white text-base font-bold leading-tight">Everyday Life</h2>
          </div>
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 items-center">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg w-10 shrink-0"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/cb79558c-bdfb-4611-8c7b-002fb7b44286.png")' }}
            ></div>
            <h2 className="text-white text-base font-bold leading-tight">Magic Hotel</h2>
          </div>
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 items-center">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-lg w-10 shrink-0"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/7841793d-78f0-4684-80e6-0493acb97bae.png")' }}
            ></div>
            <h2 className="text-white text-base font-bold leading-tight">I'm Still Here</h2>
          </div>
        </div>
        <div className="flex items-center gap-4 bg-[#122117] px-4 min-h-14 justify-between">
          <p className="text-white text-base font-normal leading-normal flex-1 truncate">Common Top Genres</p>
          <div className="shrink-0">
            <div className="text-white flex size-7 items-center justify-center" data-icon="ArrowRight" data-size="24px" data-weight="regular">
              <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                <path d="M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z"></path>
              </svg>
            </div>
          </div>
        </div>
        <div className="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-4">
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 items-center">
            <div className="text-white" data-icon="MusicNote" data-size="24px" data-weight="regular">
              <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                <path d="M210.3,56.34l-80-24A8,8,0,0,0,120,40V148.26A48,48,0,1,0,136,184V98.75l69.7,20.91A8,8,0,0,0,216,112V64A8,8,0,0,0,210.3,56.34ZM88,216a32,32,0,1,1,32-32A32,32,0,0,1,88,216ZM200,101.25l-64-19.2V50.75L200,70Z"></path>
              </svg>
            </div>
            <h2 className="text-white text-base font-bold leading-tight">Pop</h2>
          </div>
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 items-center">
            <div className="text-white" data-icon="MusicNote" data-size="24px" data-weight="regular">
              <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                <path d="M210.3,56.34l-80-24A8,8,0,0,0,120,40V148.26A48,48,0,1,0,136,184V98.75l69.7,20.91A8,8,0,0,0,216,112V64A8,8,0,0,0,210.3,56.34ZM88,216a32,32,0,1,1,32-32A32,32,0,0,1,88,216ZM200,101.25l-64-19.2V50.75L200,70Z"></path>
              </svg>
            </div>
            <h2 className="text-white text-base font-bold leading-tight">Indie</h2>
          </div>
          <div className="flex flex-1 gap-3 rounded-lg border border-[#366346] bg-[#1b3223] p-4 items-center">
            <div className="text-white" data-icon="MusicNote" data-size="24px" data-weight="regular">
              <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                <path d="M210.3,56.34l-80-24A8,8,0,0,0,120,40V148.26A48,48,0,1,0,136,184V98.75l69.7,20.91A8,8,0,0,0,216,112V64A8,8,0,0,0,210.3,56.34ZM88,216a32,32,0,1,1,32-32A32,32,0,0,1,88,216ZM200,101.25l-64-19.2V50.75L200,70Z"></path>
              </svg>
            </div>
            <h2 className="text-white text-base font-bold leading-tight">Hip Hop</h2>
          </div>
        </div>
        <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Ariel's Favorite Artist of the Week</h2>
        <div className="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-4">
          <div className="flex flex-col gap-3 pb-3">
            <div
              className="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-xl"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/2bd87b13-cefa-4277-98db-abdd904c153f.png")' }}
            ></div>
            <p className="text-white text-base font-medium leading-normal">Coldplay</p>
          </div>
          <div className="flex flex-col gap-3 pb-3">
            <div
              className="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-xl"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/8cda9c55-7851-40dd-96d2-b12be6cd2e62.png")' }}
            ></div>
            <p className="text-white text-base font-medium leading-normal">TOPloader</p>
          </div>
          <div className="flex flex-col gap-3 pb-3">
            <div
              className="w-full bg-center bg-no-repeat aspect-square bg-cover rounded-xl"
              style={{ backgroundImage: 'url("https://cdn.usegalileo.ai/sdxl10/9eb58f58-4751-44a3-b520-88e75e53f8e1.png")' }}
            ></div>
            <p className="text-white text-base font-medium leading-normal">Peach Tree Rascals</p>
          </div>
        </div>
        <div className="h-5 bg-[#122117]"></div>
      </div>
    </div>
  );
}

export default LoginPage;