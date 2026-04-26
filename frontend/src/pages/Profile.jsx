import { useEffect, useState } from "react";
import {
  UserCircle,
  Mail,
  Calendar,
  Plane,
  Wallet,
  LogOut,
} from "lucide-react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import { useAuth } from "../context/AuthContext";
import API from "../api/axios";
import bg from "../assets/login-bg.jpg";

const Profile = () => {
  const { logout } = useAuth();

  const [profile, setProfile] = useState({
    name: "Traveler",
    email: "Not available",
    joined: new Date().toLocaleDateString(),
    totalTrips: 0,
    preferredBudget: "Medium",
  });

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const res = await API.get("/my-trips");
        const trips = res.data.trips || [];

        setProfile((prev) => ({
          ...prev,
          totalTrips: trips.length,
          preferredBudget:
            trips.length > 0
              ? trips[trips.length - 1].budget || "Medium"
              : "Medium",
        }));
      } catch (err) {
        console.log(err);
      }
    };

    fetchTrips();

    const token = localStorage.getItem("token");

    if (token) {
      try {
        const payload = JSON.parse(atob(token.split(".")[1]));

        setProfile((prev) => ({
          ...prev,
          name: payload.name || "Traveler",
          email: payload.email || "Not available",
        }));
      } catch (err) {
        console.log(err);
      }
    }
  }, []);

  const handleLogout = () => {
    logout();
    window.location.href = "/login";
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center bg-fixed"
      style={{ backgroundImage: `url(${bg})` }}
    >
      <div className="min-h-screen bg-black/60 backdrop-blur-sm">
        <Navbar />
        <Sidebar />

        <div className="pt-20">
          <main className="ml-72 min-h-screen p-10">
            <div className="max-w-5xl mx-auto bg-white/10 border border-white/10 rounded-3xl p-10 backdrop-blur-xl shadow-card">
              <div className="flex items-center gap-6 mb-10">
                <div className="w-28 h-28 rounded-full bg-sky-500 flex items-center justify-center">
                  <UserCircle size={60} />
                </div>

                <div>
                  <h1 className="text-4xl font-bold">{profile.name}</h1>
                  <p className="text-gray-300 mt-2">{profile.email}</p>
                  <span className="inline-block mt-3 px-4 py-2 bg-sky-500/20 text-sky-300 rounded-full text-sm">
                    Premium Traveler
                  </span>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <Card icon={<Calendar />} title="Member Since" value={profile.joined} />
                <Card icon={<Plane />} title="Total Trips" value={profile.totalTrips} />
                <Card icon={<Wallet />} title="Preferred Budget" value={profile.preferredBudget} />
                <Card icon={<Mail />} title="Email" value={profile.email} />
              </div>

              <button
                onClick={handleLogout}
                className="mt-10 bg-red-500 hover:bg-red-600 px-6 py-3 rounded-xl flex items-center gap-2"
              >
                <LogOut size={18} />
                Logout
              </button>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

const Card = ({ icon, title, value }) => (
  <div className="bg-white/5 rounded-2xl p-6">
    <div className="flex items-center gap-3 mb-3 text-sky-400">
      {icon}
      <h3 className="text-xl font-semibold text-white">{title}</h3>
    </div>
    <p className="text-gray-300">{value}</p>
  </div>
);

export default Profile;