const FlightCard = ({ flight }) => {
  return (
    <div className="bg-white/10 rounded-2xl p-5">
      <h3 className="font-bold text-xl">{flight.airline}</h3>
      <p>{flight.origin} → {flight.destination}</p>
      <p>₹ {flight.price || "N/A"}</p>
    </div>
  );
};

export default FlightCard;