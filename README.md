AI Travel Planner
Welcome to the AI Travel Planner! This project is a full-stack application designed to help users automatically generate and manage their travel itineraries using the power of artificial intelligence. It uses a modern React frontend and a Python backend powered by FastAPI and LangGraph.

What it does
This application acts as your personal AI travel agent. Once you create an account and log in, you can submit details about your ideal trip. The backend AI, driven by LangChain and LangGraph, will process your request and return a tailored travel itinerary. You can also save and view all your previously generated trips in a dedicated dashboard.

Tech Stack
Frontend
The user interface is built for speed and responsiveness, utilizing:

React (via Vite) for the core framework.

Tailwind CSS for styling.

Framer Motion for smooth, interactive animations.

Lucide React for clean icons.

Axios for handling API requests to the backend.

Backend
The server handles the heavy lifting, AI processing, and data storage using:

FastAPI to run a robust and speedy backend server.

LangChain and LangGraph to manage the AI agent's logic and workflow.

MongoDB (via PyMongo) to store user data and trip histories.

Redis for caching.

JWT (JSON Web Tokens) and bcrypt for secure user authentication and password hashing.

Features
Secure user authentication (sign up and log in).

AI-driven trip generation based on your custom prompts.

A personalized dashboard to view all your saved trips.

A modern, animated user interface.

Getting Started
If you want to run this project on your local machine, you will need to set up both the backend and the frontend.

Setting up the Backend
Navigate to the backend directory.

It is highly recommended to create a virtual environment for Python.

Install the required dependencies by running the following command:
pip install -r requirements.txt

Ensure you have your environment variables set up (such as database URIs and OpenAI API keys) in a .env file.

Start the FastAPI server. It will run on port 8000 by default.

Setting up the Frontend
Open a new terminal window and navigate to the frontend directory.

Install the necessary node modules by running:
npm install

Once the installation is complete, start the development server using:
npm run dev

The frontend will typically be accessible at http://localhost:5173.

The frontend is already configured to communicate with the backend running on your local machine, so once both servers are up, you should be ready to start planning trips!
