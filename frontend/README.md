# Frontend

This directory contains a small Next.js application that talks to the FastAPI backend located in `../api`.

## Local development

1. Install dependencies (requires `npm`):
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`.

## Building for production

```
npm run build
npm start
```

## Deployment

The project is configured to deploy on Vercel using the `vercel` CLI. Run `vercel` and follow the prompts. Make sure your backend API key is supplied in the UI when prompted.

