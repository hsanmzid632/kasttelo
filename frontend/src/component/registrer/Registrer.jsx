// src/pages/Register.jsx

import { useState } from 'react';
import './Registrer.css'; // Attention à l'orthographe du fichier CSS !
import { register } from '../../auth'; // Ce fichier doit contenir ta logique d'appel API
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import Logo from '../../assets/logo.png'; // Ton logo

function Register() {
    const navigate = useNavigate();
    const [form, setForm] = useState({ username: '', email: '', password: '' });
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await register(form.username, form.email, form.password);
            alert('Compte créé avec succès !');
            navigate('/login');
        } catch (err) {
            console.error(err);
            setError("Erreur lors de la création du compte.");
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <div className="logo-container">
                    <img src={Logo} alt="Logo" className="logo" />
                </div>
                <h2 className="login-title">Créer un compte</h2>
                <form onSubmit={handleSubmit} className="login-form">
                    <label>Nom d'utilisateur</label>
                    <input
                        type="text"
                        name="username"
                        placeholder="Nom d'utilisateur"
                        value={form.username}
                        onChange={handleChange}
                        required
                    />

                    <label>Email</label>
                    <input
                        type="email"
                        name="email"
                        placeholder="Adresse email"
                        value={form.email}
                        onChange={handleChange}
                        required
                    />

                    <label>Mot de passe</label>
                    <input
                        type="password"
                        name="password"
                        placeholder="Mot de passe"
                        value={form.password}
                        onChange={handleChange}
                        required
                    />

                    <button type="submit">S'inscrire</button>

                    {error && <p className="error-message">{error}</p>}
                    <div className="login-footer">
                        Déjà un compte ? <Link to="/login">
                            <button>Se connecter</button>
                        </Link>
                    </div>
                </form>

            </div>
        </div>
    );
}

export default Register;
