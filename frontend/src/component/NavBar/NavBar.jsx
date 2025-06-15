// src/components/Navbar.jsx
import React from 'react';
import './NavBar.css';
import { useNavigate } from 'react-router-dom';
import Logo from '../../assets/logo.png';

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Tu peux ici supprimer des infos user si tu en ajoutes plus tard
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo" onClick={() => navigate('/home')}>
        <img src={Logo} alt="Logo" />
      </div>

      <div className="navbar-links">
        <button onClick={handleLogout}>Déconnexion</button>
      </div>
    </nav>
  );
};

export default Navbar;
