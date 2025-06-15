import './App.css';
import Login from './component/login/LoginRegister.jsx'; // import login component
import Home from './component/Home/Home';
import { Routes, Route } from 'react-router-dom'; // import BrowserRouter, Routes and Route from react-router-dom
import Register from './component/registrer/Registrer.jsx'; // import register component
import { Navigate } from 'react-router-dom'; // import Navigate from react-router-dom

function App() {
  return (
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/register" element={<Register />} />
      </Routes>
  );
}

export default App;
