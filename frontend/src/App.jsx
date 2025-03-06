import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import OLD_LandingPage from './components/OLD_DELETE_LandingPage/LandingPage';
import LoginPage from './components/Login_Signup/LoginPage';
import About from './components/About/About';
import QuickNav from './components/QuickNav/QuickNav';
import Dashboard from './components/Dashboard/MainLayout';
import Profile from './components/Profile/SpotifyProfile';

const isAuthenticated = true; //replace with authentication check later

function App() {

  return (
    <BrowserRouter>
      <div>
        <Routes>
          <Route path="/" element={isAuthenticated ? <LandingPage /> : <Navigate to="/EvanTest" />} /> 
          {/*If logged in, go to homepage, else go to Landing page by default*/}

          <Route path="/EvanTest" element={<LandingPage/>}/>
          <Route path="/Welcome" element={<OLD_LandingPage />} />
          {/*Simple directory page, Login, Sign-up, About*/}
          <Route path="/Login" element={<LoginPage />}/>
          <Route path="/About" element={<About />}/>
          <Route path="/QuickNav" element={<QuickNav />}/>
          <Route path="/MatchingPageDesktop" element={<Dashboard />}/>
          <Route path="/Profile" element={<Profile />}/>

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
