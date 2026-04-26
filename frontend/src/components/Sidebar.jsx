import { LayoutDashboard, Map, User } from "lucide-react";
import { NavLink } from "react-router-dom";

const Sidebar = () => {
  const link =
    "flex items-center gap-3 px-5 py-4 rounded-xl hover:bg-white/10 transition";

  return (
    <aside className="fixed left-0 top-20 bottom-0 w-72 p-6 border-r border-white/10 bg-black/20 backdrop-blur-xl z-40">
      <div className="space-y-3">
        <NavLink to="/dashboard" className={link}>
          <LayoutDashboard size={20} />
          Dashboard
        </NavLink>

        <NavLink to="/my-trips" className={link}>
          <Map size={20} />
          My Trips
        </NavLink>

        <NavLink to="/profile" className={link}>
          <User size={20} />
          Profile
        </NavLink>
      </div>
    </aside>
  );
};

export default Sidebar;