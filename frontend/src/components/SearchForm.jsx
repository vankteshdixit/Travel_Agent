import { useState } from "react";
import {
  MapPin,
  PlaneTakeoff,
  Calendar,
  Clock3,
  IndianRupee,
  Sparkles,
} from "lucide-react";
import API from "../api/axios";
import { useNavigate } from "react-router-dom";

const SearchForm = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    origin: "",
    destination: "",
    travel_date: "",
    days: 3,
    budget: "medium",
  });

  const [loading, setLoading] = useState(false);

  const handle = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const setBudget = (budget) => {
    setForm({
      ...form,
      budget,
    });
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await API.post("/trip-request", form);

      navigate("/trip-results", {
        state: res.data,
      });
    } catch (err) {
      alert("Trip generation failed");
    } finally {
      setLoading(false);
    }
  };

  const budgetCard = (type, title, desc) => (
    <button
      type="button"
      onClick={() => setBudget(type)}
      className={`p-5 rounded-2xl border transition text-left ${
        form.budget === type
          ? "bg-sky-500 border-sky-400 shadow-glow"
          : "bg-white/5 border-white/10 hover:bg-white/10"
      }`}
    >
      <div className="font-bold text-lg">{title}</div>
      <div className="text-sm text-gray-300 mt-1">{desc}</div>
    </button>
  );

  return (
    <form
      onSubmit={submit}
      className="bg-white/10 backdrop-blur-xl border border-white/10 rounded-[30px] p-10 shadow-card"
    >
      <h2 className="text-4xl font-bold mb-2">
        Build Your Journey ✈️
      </h2>

      <p className="text-gray-300 mb-10">
        Smart AI planning with flights, hotels and itinerary.
      </p>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="relative">
          <PlaneTakeoff className="absolute left-4 top-4 text-sky-400" />
          <input
            name="origin"
            placeholder="From"
            required
            onChange={handle}
            className="w-full bg-white/10 rounded-2xl pl-14 pr-4 py-4 outline-none border border-white/10 focus:border-sky-400"
          />
        </div>

        <div className="relative">
          <MapPin className="absolute left-4 top-4 text-sky-400" />
          <input
            name="destination"
            placeholder="To"
            required
            onChange={handle}
            className="w-full bg-white/10 rounded-2xl pl-14 pr-4 py-4 outline-none border border-white/10 focus:border-sky-400"
          />
        </div>

        <div className="relative">
          <Calendar className="absolute left-4 top-4 text-sky-400" />
          <input
            type="date"
            name="travel_date"
            required
            onChange={handle}
            className="w-full bg-white/10 rounded-2xl pl-14 pr-4 py-4 outline-none border border-white/10 focus:border-sky-400"
          />
        </div>

        <div className="relative">
          <Clock3 className="absolute left-4 top-4 text-sky-400" />
          <input
            type="number"
            min="1"
            max="30"
            value={form.days}
            name="days"
            onChange={handle}
            className="w-full bg-white/10 rounded-2xl pl-14 pr-4 py-4 outline-none border border-white/10 focus:border-sky-400"
          />
        </div>
      </div>

      <div className="mt-10">
        <div className="flex items-center gap-2 mb-5">
          <IndianRupee className="text-sky-400" />
          <h3 className="text-xl font-semibold">Budget</h3>
        </div>

        <div className="grid md:grid-cols-3 gap-5">
          {budgetCard("low", "Low", "Budget friendly trip")}
          {budgetCard("medium", "Medium", "Balanced comfort")}
          {budgetCard("high", "High", "Luxury premium stay")}
        </div>
      </div>

      <button
        className="mt-10 w-full bg-gradient-to-r from-sky-500 to-cyan-400 py-5 rounded-2xl text-lg font-bold hover:scale-[1.02] transition flex justify-center items-center gap-3"
      >
        <Sparkles />
        {loading ? "Generating..." : "Generate AI Trip"}
      </button>
    </form>
  );
};

export default SearchForm;