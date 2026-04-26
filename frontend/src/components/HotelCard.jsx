const HotelCard = ({ hotel }) => {
  return (
    <div className="bg-white/10 rounded-2xl p-5">
      <h3 className="font-bold text-xl">{hotel.name}</h3>
      <p>⭐ {hotel.rating || "N/A"}</p>
      <p>₹ {hotel.price || "N/A"}</p>
    </div>
  );
};

export default HotelCard;