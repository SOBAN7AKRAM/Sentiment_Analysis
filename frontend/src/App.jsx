import React from "react";
import { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import SignupPage from "./pages/SignupPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import PredictPage from "./pages/PredictPage.jsx";
import axios from "axios";

const BASE_URL = 'http://localhost:8000/'


// Simple authentication check
const isAuthenticated = () => !!localStorage.getItem("accessToken");

const ProtectedRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};



const Header = () => {
  const navigate = useNavigate();
  const auth = !!localStorage.getItem("access");

  const handleLogout = async () => {
    const accessToken = localStorage.getItem("access");

    try {
      // Optional: Call logout endpoint to blacklist or revoke token
      await axios.post(
        `${BASE_URL}/api/logout`,
        {"refresh": localStorage.getItem("refresh")},
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
        }
      );
    } catch (error) {
      console.error("Logout failed:", error.response?.data || error.message);
    }

    // Clear tokens locally regardless of API result
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/login");
  };

  return (
    <header className="bg-gray-800 text-white px-6 py-4 flex justify-between items-center">
      <h1
        className="text-2xl font-semibold cursor-pointer"
        onClick={() => navigate("/predict")}
      >
        Sentiment AI
      </h1>
      <div className="space-x-4">
        {!auth ? (
          <>
            <button
              onClick={() => navigate("/signup")}
              className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded"
            >
              Sign Up
            </button>
            <button
              onClick={() => navigate("/login")}
              className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded"
            >
              Log In
            </button>
          </>
        ) : (
          <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded"
          >
            Logout
          </button>
        )}
      </div>
    </header>
  );
};

const App = () => {
  useEffect(() => {
    const fetchCSRFToken = async () => {
      try {
        console.log("Runnnnn............................")
        const res = await axios.get(`${BASE_URL}/api/csrf/`, { withCredentials: true });
        console.log(res)
        localStorage.setItem('csrfToken', res.data.csrfToken);  // Store CSRF token if needed
      } catch (err) {
        console.log(err)
      }
    };
  
    fetchCSRFToken();
  }, []);

  return (
    <Router>
      <Header />
      <main className="p-4">
        <Routes>
          <Route path="/" element={<Navigate to="/predict" />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/predict"
            element={
              <ProtectedRoute>
                <PredictPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </Router>
  );
};

export default App;
