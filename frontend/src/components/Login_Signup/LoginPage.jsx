import React from 'react'
import { Link } from 'react-router-dom';

function LoginPage() {
  return (
    <div>
      <h1>The Lorax</h1>
      <Link to="/Home"><button className='btn'>Back</button></Link>

    </div>
    
  )
}

export default LoginPage