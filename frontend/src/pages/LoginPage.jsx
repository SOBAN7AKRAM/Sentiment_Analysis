import { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';


const BASE_URL = 'http://localhost:8000/'


export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();


  const login = async () => {
    try {
      const res = await axios.post(`${BASE_URL}/api/login`, { email, password });
      localStorage.setItem('access', res.data.tokens.access);
      localStorage.setItem('refresh', res.data.tokens.refresh);
      setMessage('Login successful');
      navigate('/predict'); // ✅ redirect after success


    } catch (err) {
      console.log(err.response.data.error)
      setMessage(err.response.data.error || 'Login failed');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-8 bg-white rounded-2xl shadow-lg">
      <h1 className="text-3xl font-semibold mb-6 text-center">Login to Your Account</h1>
  
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
      />
  
      <input
        type="password"
        placeholder="Enter your password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
      />
  
      <button
        onClick={login}
        className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition"
      >
        Login
      </button>
  
      {message && <p className="text-center mt-4 text-red-600">{message}</p>}
      <div className="mt-6 text-center text-gray-500">
      <div className="mb-2">-------------------------- OR --------------------------</div>
      <p>
        Don't have an account?{' '}
        <Link to="/signup" className="text-blue-600 hover:underline">
          Register
        </Link>
      </p>
    </div>


    </div>
  );
  
}
