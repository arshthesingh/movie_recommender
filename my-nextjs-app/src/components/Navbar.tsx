'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, [pathname]); 
  

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    router.push('/login');
  };

  return (
    <nav className="w-full bg-gray-800 text-white py-3 px-4 flex items-center justify-between">
      <Link href="/" className="text-xl font-semibold">
        My Movie App
      </Link>
      <div className="space-x-4">
        {!isLoggedIn && (
          <>
            <Link href="/login" className="hover:text-gray-300">
              Login
            </Link>
            <Link href="/register" className="hover:text-gray-300">
              Register
            </Link>
          </>
        )}
        {isLoggedIn && (
          <>
            <Link href="/recommendations" className="hover:text-gray-300">
              Recommendations
            </Link>
            <button onClick={handleLogout} className="hover:text-gray-300">
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
}
