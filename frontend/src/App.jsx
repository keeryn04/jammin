import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage/LandingPageContainer';
import LoginContainer from './components/LoginPage/LoginContainer';
import ErrorContainer from './components/ErrorPage/ErrorContainer';
import Dashboard from './components/Dashboard/MainLayout';
import SpotifyProfile from './components/Profile/SpotifyProfile';
import PublicProfile from './components/PublicProfile/ProfileLayout'
import JamminProfile from './components/JamminProfile/ProfilePage'
import SignupContainer1 from './components/SignupPage/SignupContainer1';
import SignupContainer2 from './components/SignupPage/SignupContainer2';
import { SignupProvider } from './components/SignupPage/SignupContext';
import Matches from './components/Matches/MainDashboard';
import { UserProvider } from './components/UserContext';
import AboutContainer from './components/About Page/AboutContainer';

const isAuthenticated = true; //replace with authentication check later

function App() {

  return (
    <BrowserRouter>
    <UserProvider>
      <div>
        <Routes>
          {/*If logged in, go to homepage, else go to Landing page by default*/}
          <Route path="/" element={isAuthenticated ? <LandingPage /> : <Navigate to="/" />} />
          

          {/*Simple directory page, Login, Sign-up, About*/}
          <Route path="/Login" element={<LoginContainer />}/>
          <Route 
            path="/Signup/*" 
            element={
              <SignupProvider>
                <Routes>
                  <Route path="step1" element={<SignupContainer1/>}/>
                  <Route path="step2" element={<SignupContainer2/>}/>
                </Routes>
              </SignupProvider>
            }/>
          <Route path="/Error" element={<ErrorContainer />}/>
          <Route path="/Matching" element={<Dashboard />}/>
          <Route path="/PublicProfile" element={<PublicProfile />}/>
          <Route path="/JamminProfile" element={<JamminProfile />}/>
          <Route path="/Matches" element={<Matches />}/>
          <Route path="/About" element={<AboutContainer />}/>

          <Route path="/SpotifyProfile" element={<SpotifyProfile />}/>

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
      </UserProvider>
    </BrowserRouter>
  )
}

export default App
