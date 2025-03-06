import React from 'react'
import { Link } from 'react-router-dom';

function LandingPage() {
  return (
    <div>
        <h1>Roger, Roger, cleared for Landing</h1>
        <Link to="/Home"><button className='btn'>Back</button></Link>
        
    </div>
  )
}

export default LandingPage