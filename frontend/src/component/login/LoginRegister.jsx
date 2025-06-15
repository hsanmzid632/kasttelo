import React, { useState } from 'react';
import './LoginPage.css';
import '../../assets/bg.png';
import Logo from '../../assets/logo.png';
import { useNavigate } from 'react-router-dom';

const LoginRegister = () => {
    const navigate = useNavigate();
    const [isRightPanelActive, setIsRightPanelActive] = useState(false);

    const [loginData, setLoginData] = useState({ username: '', password: '' });
    const [registerData, setRegisterData] = useState({ username: '', email: '', password: '' });
    const [error, setError] = useState('');


    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/token/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(loginData),
            });

            const data = await response.json();

            if (!response.ok) {
                // Gestion des erreurs de login (ex: mauvais mot de passe)
                if (data.detail) {
                    alert(data.detail);
                    setError(data.detail);
                } else {
                    alert('Identifiants incorrects');
                    setError('Identifiants incorrects');
                }
                return;
            }

            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            navigate('/home');
        } catch (err) {
            setError('Erreur réseau ou serveur.');
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/api/accounts/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(registerData),
            });
            const data = await response.json();
            if (!response.ok) {
                // Affiche toutes les erreurs reçues (ex: mot de passe)
                if (data.password) {
                    data.password.forEach(msg => alert(msg));
                    setError(data.password.join(' '));
                } else if (data.username) {
                    data.username.forEach(msg => alert(msg));
                    setError(data.username.join(' '));
                } else if (data.email) {
                    data.email.forEach(msg => alert(msg));
                    setError(data.email.join(' '));
                } else {
                    alert('Erreur lors de la création du compte.');
                    setError('Erreur lors de la création du compte.');
                }
                return;
            }
            alert('Compte créé avec succès !');
            setIsRightPanelActive(false);
        } catch (err) {
            setError('Erreur réseau ou serveur.');
        }
    };

    return (
        <div className='body'>
        <div className={`container ${isRightPanelActive ? 'right-panel-active' : ''}`}>

            <div className="form-container sign-up-container">
                <form onSubmit={handleRegister}>
                    <div className="logo-container">
                        <img src={Logo} alt="Logo" className="logo" />
                    </div>
                    {/* <h1>Créer un compte</h1> */}
                    <input type="text" placeholder="Nom d'utilisateur" name="username" value={registerData.username} onChange={(e) => setRegisterData({ ...registerData, username: e.target.value })} required />
                    <input type="email" placeholder="Email" name="email" value={registerData.email} onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })} required />
                    <input type="password" placeholder="Mot de passe" name="password" value={registerData.password} onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })} required />
                    <button type="submit">S'inscrire</button>
                </form>
            </div>

            <div className="form-container sign-in-container">
                <form onSubmit={handleLogin}>
                    <div className="logo-container">
                        <img src={Logo} alt="Logo" className="logo" />
                    </div>
                    {/* <h1>Connexion</h1> */}
                    <input type="text" placeholder="Nom d'utilisateur" name="username" value={loginData.username} onChange={(e) => setLoginData({ ...loginData, username: e.target.value })} required />
                    <input type="password" placeholder="Mot de passe" name="password" value={loginData.password} onChange={(e) => setLoginData({ ...loginData, password: e.target.value })} required />
                    <button type="submit">Se connecter</button>
                    {error && <p className="error-message">{error}</p>}
                </form>
            </div>

            <div className="overlay-container">
                <div className="overlay">
                    <div className="overlay-panel overlay-left">
                        <h1>Bienvenue !</h1>
                        <p>Vous avez déjà un compte ?</p>
                        <button className="ghost" onClick={() => setIsRightPanelActive(false)}>
                            Se connecter
                        </button>
                    </div>
                    <div className="overlay-panel overlay-right">
                        <h1>Bonjour !</h1>
                        <p>Vous n'avez pas encore de compte ?</p>
                        <button className="ghost" onClick={() => setIsRightPanelActive(true)}>
                            Créer un compte
                        </button>
                    </div>
                </div>
            </div>
        </div>
        </div>
    );
};

export default LoginRegister;
