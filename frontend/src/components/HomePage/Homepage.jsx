import React from 'react'
import { Link } from 'react-router-dom';

function Homepage() {
  return (
    <div>
      <h1>HOME SWEET HOME</h1>

      <div className='button-series'>
        <Link to="/Login"><button className='btn'>Login</button></Link>
        <Link to="/About"><button className='btn'>About</button></Link>
        <Link to="/Welcome"><button className='btn'>Landing Page</button></Link>
      </div>
    </div>

    
  )
}

export default Homepage