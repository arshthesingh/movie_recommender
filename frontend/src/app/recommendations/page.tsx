'use client';

import React, { useState, useEffect } from 'react';
import axios from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function RecommendationsPage() {
  const router = useRouter();
  const [title, setTitle] = useState('');
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    // If no token, redirect to login
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    }
  }, [router]);

  const handleGetRecommendations = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setRecommendations([]);

    try {
      const res = await axios.get('/api/recommendations', {
        params: { title },
      });
      setRecommendations(res.data);
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Something went wrong');
    }
  };

  
  const addTypedMovieToWatchlist = async () => {
    try {
      await axios.post('/api/watchlist/add', { movie_title: title });
      alert(`${title} added to watchlist!`);
    } catch (err: any) {
      alert(err?.response?.data?.error || 'Failed to add to watchlist');
    }
  };

  
  const addRecommendedMovieToWatchlist = async (movieTitle: string) => {
    try {
      await axios.post('/api/watchlist/add', { movie_title: movieTitle });
      alert(`${movieTitle} added to watchlist!`);
    } catch (err: any) {
      alert(err?.response?.data?.error || 'Failed to add to watchlist');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-6">Movie Recommendations</h2>

      <form onSubmit={handleGetRecommendations} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Movie Title</label>
          <input
            type="text"
            className="w-full p-2 border rounded text-black bg-white"
            placeholder="Enter a movie title..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </div>

        <div className="flex space-x-4">
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Get Recommendations
          </button>
          {}
          <button
            type="button"
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            onClick={addTypedMovieToWatchlist}
          >
            Add to Watchlist
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mt-4">{error}</div>
      )}

      {recommendations.length > 0 && (
        <div className="mt-6">
          <h3 className="text-xl font-semibold mb-3">Recommendations:</h3>
          <ul className="list-disc list-inside space-y-2">
            {recommendations.map((movie, idx) => (
              <li key={idx} className="flex items-center justify-between">
                <span>{movie}</span>
                <button
                  onClick={() => addRecommendedMovieToWatchlist(movie)}
                  className="ml-4 px-2 py-1 bg-green-500 text-white rounded hover:bg-green-600"
                >
                  Add
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
