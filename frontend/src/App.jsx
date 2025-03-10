import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage/LandingPageContainer';
import LoginContainer from './components/LoginPage/LoginContainer';
import About from './components/About/About';
import QuickNav from './components/QuickNav/QuickNav';
import Dashboard from './components/Dashboard/MainLayout';
import Profile from './components/Profile/SpotifyProfile';
import SignupContainer1 from './components/SignupPage/SignupContainer1';
import SignupContainer2 from './components/SignupPage/SignupContainer2';

const isAuthenticated = true; //replace with authentication check later

function App() {

  return (
    <BrowserRouter>
      <div>
        <Routes>
          {/*If logged in, go to homepage, else go to Landing page by default*/}
          <Route path="/" element={isAuthenticated ? <LandingPage /> : <Navigate to="/" />} />
          

          {/*Simple directory page, Login, Sign-up, About*/}
          <Route path="/Login" element={<LoginContainer />}/>
          <Route path="/Signup1" element={<SignupContainer1/>}/>
          <Route path="/Signup2" element={<SignupContainer2/>}/>
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
