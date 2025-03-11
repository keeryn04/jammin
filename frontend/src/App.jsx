import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage1/LandingPage';
import About from './components/About/About';
import QuickNav from './components/ErrorPage/QuickNav';
import Dashboard from './components/Dashboard/MainLayout';
import SpotifyProfile from './components/Profile/SpotifyProfile';
import PublicProfile from './components/PublicProfile/ProfileLayout'
import JamminProfile from './components/JamminProfile/ProfilePage'

const isAuthenticated = true; //replace with authentication check later

function App() {

  return (
    <BrowserRouter>
      <div>
        <Routes>
          <Route path="/" element={isAuthenticated ? <LandingPage /> : <Navigate to="/EvanTest" />} /> 
          {/*If logged in, go to homepage, else go to Landing page by default*/}

          <Route path="/EvanTest" element={<LandingPage/>}/>
          {/*Simple directory page, Login, Sign-up, About*/}
          <Route path="/About" element={<About />}/>
          <Route path="/QuickNav" element={<QuickNav />}/>
          <Route path="/Matching" element={<Dashboard />}/>
          <Route path="/PublicProfile" element={<PublicProfile />}/>
          <Route path="/JamminProfile" element={<JamminProfile />}/>


          <Route path="/SpotifyProfile" element={<SpotifyProfile />}/>

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
