import React, { useState } from 'react';
import Navbar from '../NavBar/NavBar';
import './Home.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Circles } from 'react-loader-spinner';

const Home = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [previewImage, setPreviewImage] = useState('');
    const [similarImages, setSimilarImages] = useState([]);
    const [doSimilaritySearch, setDoSimilaritySearch] = useState(false);
    const [loading, setLoading] = useState(false);
    const [googleLensResults, setGoogleLensResults] = useState([]);
    const [articleInfos, setArticleInfos] = useState({});

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedImage(file);
            setPreviewImage(URL.createObjectURL(file));
            setSimilarImages([]);
        }
    };


    const fetchArticleInfos = async (codes) => {
        try {
            const res = await fetch('http://localhost:8000/api/article_infos/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ codes }),
            });
            if (!res.ok) throw new Error('Erreur infos articles');
            const data = await res.json();
            setArticleInfos(data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleSubmit = async () => {
        if (!selectedImage) {
            toast.warning("Veuillez sélectionner une image.");
            return;
        }
        setLoading(true);
        setGoogleLensResults([]);
        const formData = new FormData();
        formData.append("image", selectedImage);

        try {
            // Recherche par similarité locale (toujours)
            const res = await fetch('http://localhost:8000/api/similar/', {
                method: 'POST',
                body: formData,
            });
            if (!res.ok) throw new Error('Erreur de recherche');
            const data = await res.json();
            setSimilarImages(data.results);
            // Récupérer les infos articles après la recherche
            const codes = data.results.map(img => img.code_article);
            fetchArticleInfos(codes);

            // Si la case est cochée, simuler une recherche Google Lens
            if (doSimilaritySearch) {
                // Ici, on simule un appel à Google Lens (remplace par un vrai appel si tu as une API)
                setTimeout(() => {
                    setGoogleLensResults([
                        { title: 'Source 1', url: 'https://lens.google.com/result1' },
                        { title: 'Source 2', url: 'https://lens.google.com/result2' },
                        { title: 'Source 3', url: 'https://lens.google.com/result3' },
                    ]);
                    toast.info('Résultats Google Lens affichés.');
                }, 1200);
            }

            toast.success("Recherche terminée !");
        } catch (err) {
            console.error(err);
            toast.error("Une erreur s'est produite.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <Navbar />
            <div className="home-container">


                <div className="card">
                    <h2>🔍 Recherche par Similarité d’Images</h2>
                    <label className="upload-label">Choisissez une image :</label>
                    <input
                        className="upload-input"
                        type="file"
                        accept="image/*"
                        onChange={handleImageChange}
                    />

                    {previewImage && (
                        <div className="preview-section">
                            <img src={previewImage} alt="Aperçu" className="preview-img" />
                        </div>
                    )}

                    <div className="options">
                        <label className="checkbox-container">
                            <input
                                type="checkbox"
                                checked={doSimilaritySearch}
                                onChange={() => setDoSimilaritySearch(!doSimilaritySearch)}
                            />{' '}
                            Activer la recherche Google Lens (sources externes)
                        </label>
                    </div>

                    <button className="submit-btn" onClick={handleSubmit} disabled={loading}>
                        {loading ? "Recherche..." : "🔎 Lancer la recherche"}
                    </button>

                    {loading && (
                        <div style={{ marginTop: '1.5rem' }}>
                            <Circles
                                height="60"
                                width="60"
                                color="#4fa94d"
                                ariaLabel="circles-loading"
                                visible={true}
                            />
                        </div>
                    )}
                    <div className="similar-container">
                        {similarImages.map((img, i) => (
                            <div key={i} className="similar-card">
                                <div style={{ fontWeight: "bold", marginBottom: "0.5rem" }}>
                                    {img.code_article}
                                </div>
                                {img.path ? (
                                    <img
                                        src={`http://localhost:8000/${img.path}`}
                                        alt={`sim${i + 1}`}
                                    />
                                ) : (
                                    <div>Image non trouvée</div>
                                )}
                                <p>
                                    Distance :{" "}
                                    {typeof img.distance === "number"
                                        ? img.distance.toFixed(4)
                                        : "N/A"}
                                </p>
                                {articleInfos[img.code_article] && (
                                    <>
                                        <p>Ventes : {articleInfos[img.code_article].quantite}</p>
                                        <p>Saisonnalité : {articleInfos[img.code_article].collection}</p>
                                    </>
                                )}
                            </div>
                        ))}
                    </div>
                    {doSimilaritySearch && googleLensResults.length > 0 && (
                        <div className="google-lens-section" style={{ marginTop: 24 }}>
                            <h3>🔗 Sources Google Lens</h3>
                            <ul>
                                {googleLensResults.map((src, idx) => (
                                    <li key={idx}>
                                        <a href={src.url} target="_blank" rel="noopener noreferrer">{src.title}</a>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            </div>
            <ToastContainer position="top-right" autoClose={3000} hideProgressBar />
        </div>
    );
};

export default Home;
