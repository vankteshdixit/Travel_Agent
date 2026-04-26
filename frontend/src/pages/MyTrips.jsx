import { useEffect, useState } from "react";
import { Calendar, Wallet, Plane } from "lucide-react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import bg from "../assets/login-bg.jpg";

const MyTrips = () => {
  const [trips, setTrips] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        const res = await API.get("/my-trips");
        setTrips(res.data.trips || []);
      } catch (err) {
        console.log(err);
      }
    };

    fetchTrips();
  }, []);

  const openTrip = (trip) => {
    navigate("/trip-results", {
      state: trip,
    });
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
            <h1 className="text-4xl font-bold mb-10">My Trips</h1>

            {trips.length === 0 ? (
              <div className="bg-white/10 rounded-3xl p-10 text-center text-gray-300">
                No trips planned yet.
              </div>
            ) : (
              <div className="grid md:grid-cols-2 gap-8">
                {trips.map((trip, i) => (
                  <div
                    key={i}
                    onClick={() => openTrip(trip)}
                    className="cursor-pointer bg-white/10 border border-white/10 rounded-3xl p-7 hover:bg-white/15 hover:scale-[1.02] transition duration-300"
                  >
                    <div className="flex justify-between items-start mb-5">
                      <h2 className="text-2xl font-bold">
                        {trip.origin} → {trip.destination}
                      </h2>

                      <Plane className="text-sky-400" />
                    </div>

                    <div className="space-y-3 text-gray-300">
                      <div className="flex items-center gap-3">
                        <Calendar size={18} />
                        <span>{trip.travel_date}</span>
                      </div>

                      <div>
                        Duration: <span className="text-white">{trip.days} days</span>
                      </div>

                      <div className="flex items-center gap-3">
                        <Wallet size={18} />
                        <span className="capitalize">{trip.budget}</span>
                      </div>
                    </div>

                    <button className="mt-6 w-full bg-sky-500 hover:bg-sky-600 rounded-xl py-3 font-semibold">
                      View Details
                    </button>
                  </div>
                ))}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default MyTrips;