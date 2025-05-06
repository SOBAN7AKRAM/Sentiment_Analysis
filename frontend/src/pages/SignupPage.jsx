import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000/';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [password, setPassword] = useState('');
  const [step, setStep] = useState(1);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const sendOtp = async () => {
    try {
      await axios.post(`${BASE_URL}/api/send_otp`, { email }, {
        headers: {
          "X-CSRFToken": localStorage.getItem('csrfToken'),
        },
        withCredentials: true,
      });
      setStep(2);
      setMessage('OTP sent to your email');
    } catch (err) {
      setMessage(err.response?.data?.error || 'Failed to send OTP');
    }
  };

  const verifyOtp = async () => {
    try {
      await axios.post(`${BASE_URL}/api/verify_otp`, { email, otp }, {
        headers: {
          "X-CSRFToken": localStorage.getItem('csrfToken'),
        },
        withCredentials: true,
      });
      setStep(3);
      setMessage('OTP verified');
    } catch (err) {
      setMessage(err.response?.data?.error || 'OTP verification failed');
    }
  };

  const signup = async () => {
    try {
      const res = await axios.post(`${BASE_URL}/api/sign_up`, { email, password }, {
        headers: {
          "X-CSRFToken": localStorage.getItem('csrfToken'),
        },
        withCredentials: true,
      });
      localStorage.setItem('access', res.data.tokens.access);
      localStorage.setItem('refresh', res.data.tokens.refresh);
      setMessage('Signup successful');
      navigate('/predict'); // ✅ redirect after success
    } catch (err) {
      setMessage(err.response?.data?.error || 'Signup failed');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-8 bg-white rounded-2xl shadow-lg">
      <h1 className="text-3xl font-semibold mb-6 text-center">Create Your Account</h1>

      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
      />

      {step >= 2 && (
        <input
          type="text"
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          className="w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
        />
      )}

      {step === 3 && (
        <input
          type="password"
          placeholder="Set your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
        />
      )}

      {step === 1 && (
        <button
          onClick={sendOtp}
          className="w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition"
        >
          Send OTP
        </button>
      )}

      {step === 2 && (
        <button
          onClick={verifyOtp}
          className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
        >
          Verify OTP
        </button>
      )}

      {step === 3 && (
        <button
          onClick={signup}
          className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition"
        >
          Sign Up
        </button>
      )}

      {message && <p className="text-center mt-4 text-red-600">{message}</p>}

      <div className="mt-6 text-center text-gray-500">
      <div className="mb-2">-------------------------- OR --------------------------</div>
      <p>
        Already have an account?{' '}
        <Link to="/login" className="text-blue-600 hover:underline">
          LogIn
        </Link>
      </p>
    </div>
    </div>
  );
}
