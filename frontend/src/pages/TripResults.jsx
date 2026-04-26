import { useLocation, Navigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import FlightCard from "../components/FlightCard";
import HotelCard from "../components/HotelCard";
import Itinerary from "../components/Itinerary";
import bg from "../assets/login-bg.jpg";

const TripResults = () => {
  const location = useLocation();
  const trip = location.state;

  if (!trip) {
    return <Navigate to="/dashboard" />;
  }

  return (
    <div
      className="min-h-screen bg-cover bg-center bg-fixed"
      style={{
        backgroundImage: `url(${bg})`,
      }}
    >
      <div className="min-h-screen bg-black/60 backdrop-blur-sm">
        <Navbar />
        <Sidebar />

        <div className="pt-20">
          <main className="ml-72 min-h-screen p-10 space-y-10">
            <section>
              <h2 className="text-3xl font-bold mb-5">Flights</h2>

              <div className="grid md:grid-cols-2 gap-5">
                {trip.flights?.map((flight, i) => (
                  <FlightCard key={i} flight={flight} />
                ))}
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-bold mb-5">Hotels</h2>

              <div className="grid md:grid-cols-2 gap-5">
                {trip.hotels?.map((hotel, i) => (
                  <HotelCard key={i} hotel={hotel} />
                ))}
              </div>
            </section>

            <section>
              <h2 className="text-3xl font-bold mb-5">Itinerary</h2>
              <Itinerary text={trip.itinerary} />
            </section>
          </main>
        </div>
      </div>
    </div>
  );
};

export default TripResults;