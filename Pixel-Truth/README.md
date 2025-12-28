# Pixel Truth - Frontend

This is the frontend application for the Pixel Truth image authenticity verification platform.

## Features

- Modern React-based user interface
- Image upload and analysis
- Real-time results display
- Responsive design with Tailwind CSS
- Demo mode for testing without backend

## Tech Stack

- **React 18** - Frontend framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Dropzone** - File upload component
- **React Toastify** - Notifications
- **Lucide React** - Icons

## Prerequisites

- Node.js (version 16 or higher)
- npm (version 8 or higher)

## Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
```

3. Configure the environment variables in `.env.local`:
```
VITE_API_URL=http://localhost:5000/api
VITE_DEMO_MODE=false
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Build

Create a production build:
```bash
npm run build
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Environment Variables

- `VITE_API_URL` - Backend API URL (default: http://localhost:5000/api)
- `VITE_DEMO_MODE` - Enable demo mode (default: false)

## Demo Mode

The frontend includes a demo mode that simulates backend responses for testing purposes. Enable it by setting `VITE_DEMO_MODE=true` in your environment variables.

## Deployment

The frontend can be deployed to any static hosting service like Vercel, Netlify, or AWS S3.

For Vercel deployment, the `vercel.json` configuration is already included.

## License

MIT License