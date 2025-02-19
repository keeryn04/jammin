import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Homepage from './components/HomePage/Homepage';
import LandingPage from './components/LandingPage/LandingPage';
import LoginPage from './components/Login_Signup/LoginPage';
import About from './components/About/About';

const isAuthenticated = true; //replace with authentication check later

function App() {

  return (
    <BrowserRouter>
      <div>
        <Routes>
          <Route path="/" element={isAuthenticated ? <Homepage /> : <Navigate to="/Login" />} /> 
          {/*If logged in, go to homepage, else go to Landing page by default*/}

          <Route path="/Home" element={<Homepage />} />
          {/*This is where the magics gonna happen, will contain child page, Dashboard*/}
          <Route path="/Welcome" element={<LandingPage />} />
          {/*Simple directory page, Login, Sign-up, About*/}
          <Route path="/Login" element={<LoginPage />}/>
          <Route path="/About" element={<About />}/>
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
