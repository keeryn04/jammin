import React from 'react'
import { Link } from 'react-router-dom';

function QuickNav() {
  return (
    <div>
      <h3>Im the Flashhh</h3>
      <Link to="/Home"><button className='btn'>Home</button></Link>
      <Link to="/Login"><button className='btn'>Login</button></Link>
      <Link to="/About"><button className='btn'>About</button></Link>
      <Link to="/Welcome"><button className='btn'>Landing Page</button></Link>


    </div>
    
  )
}

export default QuickNav