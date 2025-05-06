import { useState } from 'react';
import axios from 'axios';

const BASE_URL = 'http://localhost:8000/';

const platforms = [
  'Borderlands', 'CallOfDutyBlackopsColdWar', 'Amazon', 'Overwatch',
  'Xbox(Xseries)', 'NBA2K', 'Dota2', 'PlayStation5(PS5)', 'WorldOfCraft',
  'CS-GO', 'Google', 'AssassinsCreed', 'ApexLegends', 'LeagueOfLegends',
  'Fortnite', 'Microsoft', 'Hearthstone', 'Battlefield',
  'PlayerUnknownsBattlegrounds(PUBG)', 'Verizon', 'HomeDepot', 'FIFA',
  'RedDeadRedemption(RDR)', 'CallOfDuty', 'TomClancysRainbowSix', 'Facebook',
  'GrandTheftAuto(GTA)', 'MaddenNFL', 'johnson&johnson', 'Cyberpunk2077',
  'TomClancysGhostRecon', 'Nvidia'
];

export default function PredictPage() {
  const [text, setText] = useState('');
  const [platform, setPlatform] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const predict = async () => {
    try {
      const access = localStorage.getItem('access');
      const res = await axios.post(`${BASE_URL}/api/predict`, { text, platform }, {
        headers: { Authorization: `Bearer ${access}` }
      });
      setResult(res.data.result);
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Prediction failed');
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-12 p-8 bg-white rounded-2xl shadow-xl">
      <h1 className="text-3xl font-semibold mb-6 text-center text-gray-800">Sentiment Prediction</h1>

      <label className="block text-gray-700 mb-2 font-medium">Enter your text:</label>
      <textarea
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type the content you want analyzed..."
        className="w-full mb-6 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
      />

      <label className="block text-gray-700 mb-2 font-medium">Select platform:</label>
      <select
        value={platform}
        onChange={(e) => setPlatform(e.target.value)}
        className="w-full mb-6 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500"
      >
        <option value="">-- Choose a platform --</option>
        {platforms.map((p) => (
          <option key={p} value={p}>{p}</option>
        ))}
      </select>

      <button
        onClick={predict}
        className="w-full bg-gray-600 text-white py-3 rounded-lg font-semibold hover:bg-gray-700 transition"
      >
        Predict
      </button>

      {result && (
        <p
          className={`mt-6 font-medium break-words ${
            result === 'Positive'
              ? 'text-green-600'
              : result === 'Negative'
              ? 'text-red-600'
              : result === 'Neutral'
              ? 'text-gray-600'
              : 'text-blue-600'
          }`}
        >
          Sentiment Result: {result}
        </p>
      )}

      {error && (
        <p className="mt-6 text-red-600 font-medium">{error}</p>
      )}
    </div>
  );
}
