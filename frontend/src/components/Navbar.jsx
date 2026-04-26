import { Plane, UserCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-20 px-10 flex items-center justify-between border-b border-white/10 bg-black/30 backdrop-blur-xl">
      <div className="flex items-center gap-3">
        <Plane className="text-sky-400" size={30} />
        <h1 className="text-2xl font-bold">TravelAI</h1>
      </div>

      <div className="flex items-center gap-6">
        <button
          onClick={() => navigate("/profile")}
          className="hover:text-sky-400 transition"
        >
          <UserCircle size={28} />
        </button>

        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 px-5 py-2 rounded-xl transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;