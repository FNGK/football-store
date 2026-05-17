import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  transpilePackages: [],
  // Do not rewrite /api/* to the backend — auth and /api/v1/* use Next.js Route Handlers.
};

export default nextConfig;
