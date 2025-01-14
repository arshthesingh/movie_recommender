import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="max-w-md mx-auto text-center mt-10">
      <h1 className="text-3xl font-bold mb-6">Welcome to My Movie App</h1>
      <p className="mb-6">
        Please login or register to get personalized movie recommendations!
      </p>
      <div className="space-x-4">
        <Link
          href="/login"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Login
        </Link>

        <Link
          href="/register"
          className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
        >
          Register
        </Link>
      </div>
    </div>
  );
}
