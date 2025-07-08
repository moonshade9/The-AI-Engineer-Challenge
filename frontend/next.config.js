/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8000/api/:path*', // Proxy to FastAPI backend
      },
      {
        source: '/upload_and_ask',
        destination: 'http://127.0.0.1:8000/upload_and_ask',
      },
    ];
  },
};

module.exports = nextConfig;
