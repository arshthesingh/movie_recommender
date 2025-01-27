'use client';

import React, { useState, useEffect } from 'react';
import axios from '@/lib/api';
import { useRouter } from 'next/navigation';

interface WatchlistMovie {
  title: string;
  priority: number;
}

export default function WatchlistPage() {
  const [watchlist, setWatchlist] = useState<WatchlistMovie[]>([]);
  const [error, setError] = useState('');
  const router = useRouter();

  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    } else {
      fetchWatchlist();
    }
  }, [router]);

  // Fetch watchlist from /api/watchlist
  const fetchWatchlist = async () => {
    try {
      const res = await axios.get('/api/watchlist'); 
      setWatchlist(res.data);
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Could not fetch watchlist');
    }
  };

  const removeFromWatchlist = async (movieTitle: string) => {
    try {
      await axios.post('/api/watchlist/remove', { movie_title: movieTitle });
      fetchWatchlist(); 
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Failed to remove movie');
    }
  };

  const moveMovieUp = async (movieTitle: string) => {
    try {
      await axios.post('/api/watchlist/move-up', { movie_title: movieTitle });
      fetchWatchlist();
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Failed to move movie up');
    }
  };

  const moveMovieDown = async (movieTitle: string) => {
    try {
      await axios.post('/api/watchlist/move-down', { movie_title: movieTitle });
      fetchWatchlist();
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Failed to move movie down');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-4 bg-white text-black rounded">
      <h2 className="text-2xl font-bold mb-6">My Watchlist</h2>

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
          {error}
        </div>
      )}

      {watchlist.length === 0 ? (
        <p>Your watchlist is empty.</p>
      ) : (
        <ul className="space-y-2">
          {watchlist.map((movie) => (
            <li
              key={movie.title}
              className="flex items-center justify-between bg-gray-100 text-black p-2 rounded"
            >
              <span>
                {movie.title} <em>(priority: {movie.priority})</em>
              </span>
              <div className="space-x-2">
                <button
                  onClick={() => moveMovieUp(movie.title)}
                  className="px-2 py-1 bg-blue-500 text-white rounded"
                >
                  ↑
                </button>
                <button
                  onClick={() => moveMovieDown(movie.title)}
                  className="px-2 py-1 bg-blue-500 text-white rounded"
                >
                  ↓
                </button>
                <button
                  onClick={() => removeFromWatchlist(movie.title)}
                  className="px-2 py-1 bg-red-500 text-white rounded"
                >
                  Remove
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
