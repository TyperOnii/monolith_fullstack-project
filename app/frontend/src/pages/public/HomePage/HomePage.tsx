import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom';

export const HomePage = () => {
  const userRole = localStorage.getItem("userRole");
  const navigate = useNavigate()

  useEffect(() => {
    if(!userRole){
        navigate("/login")
    }
  }, userRole)
  return (
    <div>HomePage</div>
  )
}
