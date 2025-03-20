import React from 'react'
import { useNavigate } from 'react-router-dom';
import Heading from '../Generic/Heading';
import ActionButton from '../Generic/ActionButton';

function ErrorContainer() {
  const navigate = useNavigate();

  const handleGoToLandingPage = () => {
    navigate("/");
  }

  return (
    <main className="flex flex-col p-10 h-screen w-screen justify-center items-center bg-neutral-800 
    overflow-y-auto [&::-webkit-scrollbar]:w-2
    [&::-webkit-scrollbar-track]:rounded-full
    [&::-webkit-scrollbar-track]:bg-gray-100
    [&::-webkit-scrollbar-thumb]:rounded-full
    [&::-webkit-scrollbar-thumb]:bg-gray-300
    dark:[&::-webkit-scrollbar-track]:bg-neutral-700
    dark:[&::-webkit-scrollbar-thumb]:bg-neutral-500">

      <Heading text={"Sorry we're in a bit of a jam right now..."}/>
      <ActionButton variant='primaryLandingPage' onClick={handleGoToLandingPage}>
        Go to Landing Page
      </ActionButton>
    </main>
    
  )
}

export default ErrorContainer