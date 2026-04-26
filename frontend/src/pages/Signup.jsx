import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Plane, User, Mail, Lock, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import bg from "../assets/login-bg.jpg";
import API from "../api/axios";
import { useAuth } from "../context/AuthContext";

const Signup = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await API.post("/auth/signup", form);

      login(res.data.access_token);

      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Signup failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center px-6"
      style={{ backgroundImage: `url(${bg})` }}
    >
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 w-full max-w-md bg-white/10 border border-white/20 backdrop-blur-xl rounded-3xl p-8 shadow-2xl"
      >
        <div className="flex items-center gap-3 justify-center mb-8">
          <Plane className="text-sky-400" size={34} />
          <h1 className="text-3xl font-bold">TravelAI</h1>
        </div>

        <h2 className="text-center text-gray-300 mb-8">
          Create your premium travel account
        </h2>

        {error && (
          <div className="bg-red-500/20 border border-red-400 text-red-200 p-3 rounded-xl mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="relative">
            <User className="absolute left-4 top-4 text-gray-300" size={18} />
            <input
              name="name"
              type="text"
              placeholder="Full Name"
              required
              onChange={handleChange}
              className="w-full bg-white/10 border border-white/20 rounded-xl pl-12 pr-4 py-4 outline-none focus:border-sky-400"
            />
          </div>

          <div className="relative">
            <Mail className="absolute left-4 top-4 text-gray-300" size={18} />
            <input
              name="email"
              type="email"
              placeholder="Email"
              required
              onChange={handleChange}
              className="w-full bg-white/10 border border-white/20 rounded-xl pl-12 pr-4 py-4 outline-none focus:border-sky-400"
            />
          </div>

          <div className="relative">
            <Lock className="absolute left-4 top-4 text-gray-300" size={18} />
            <input
              name="password"
              type="password"
              placeholder="Password"
              required
              onChange={handleChange}
              className="w-full bg-white/10 border border-white/20 rounded-xl pl-12 pr-4 py-4 outline-none focus:border-sky-400"
            />
          </div>

          <button
            disabled={loading}
            className="w-full bg-sky-500 hover:bg-sky-600 transition rounded-xl py-4 font-semibold flex items-center justify-center gap-2"
          >
            {loading ? "Creating..." : "Signup"}
            <ArrowRight size={18} />
          </button>
        </form>

        <p className="text-center text-gray-300 mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-sky-400 font-semibold">
            Login
          </Link>
        </p>
      </motion.div>
    </div>
  );
};

export default Signup;