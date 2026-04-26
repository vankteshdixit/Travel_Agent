import SearchForm from "../components/SearchForm";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import bg from "../assets/login-bg.jpg";

const Dashboard = () => {
  return (
    <div
      className="min-h-screen bg-cover bg-center bg-fixed"
      style={{
        backgroundImage: `url(${bg})`,
      }}
    >
      <div className="min-h-screen bg-black/50 backdrop-blur-sm">
        <Navbar />
        <Sidebar />

        <div className="pt-20">
          <main className="ml-72 min-h-screen p-10 flex items-center justify-center">
            <div className="w-full max-w-5xl">
              <SearchForm />
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;