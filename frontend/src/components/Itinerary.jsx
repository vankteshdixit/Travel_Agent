import ReactMarkdown from "react-markdown";
import {
  CalendarDays,
  Plane,
  Hotel,
  MapPinned,
  UtensilsCrossed,
  Wallet,
  AlertTriangle,
  Star,
} from "lucide-react";

const Itinerary = ({ text }) => {
  return (
    <div className="rounded-[32px] overflow-hidden border border-white/10 bg-white/10 backdrop-blur-xl shadow-card">
      {/* Header */}
      <div className="bg-gradient-to-r from-sky-500/30 to-cyan-400/20 px-10 py-8 border-b border-white/10">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-sky-500 flex items-center justify-center shadow-glow">
            <Plane size={30} />
          </div>

          <div>
            <h2 className="text-4xl font-bold">Smart Travel Itinerary</h2>
            <p className="text-gray-300 mt-1">
              AI generated premium travel guide
            </p>
          </div>
        </div>
      </div>

      {/* Quick tags */}
      <div className="grid md:grid-cols-4 gap-4 px-10 py-6 border-b border-white/10 bg-white/5">
        <div className="rounded-2xl bg-white/5 p-4 flex items-center gap-3">
          <CalendarDays className="text-sky-400" />
          <span>Day-wise Plan</span>
        </div>

        <div className="rounded-2xl bg-white/5 p-4 flex items-center gap-3">
          <Hotel className="text-sky-400" />
          <span>Hotels</span>
        </div>

        <div className="rounded-2xl bg-white/5 p-4 flex items-center gap-3">
          <MapPinned className="text-sky-400" />
          <span>Activities</span>
        </div>

        <div className="rounded-2xl bg-white/5 p-4 flex items-center gap-3">
          <Wallet className="text-sky-400" />
          <span>Budget Summary</span>
        </div>
      </div>

      {/* Content */}
      <div className="p-10">
        <div
          className="
            prose
            prose-invert
            max-w-none

            prose-h1:text-5xl
            prose-h1:font-bold
            prose-h1:text-sky-300
            prose-h1:mb-10

            prose-h2:text-3xl
            prose-h2:font-bold
            prose-h2:text-white
            prose-h2:bg-white/5
            prose-h2:px-6
            prose-h2:py-4
            prose-h2:rounded-2xl
            prose-h2:mb-6
            prose-h2:border
            prose-h2:border-white/10

            prose-h3:text-xl
            prose-h3:text-cyan-300
            prose-h3:font-semibold
            prose-h3:mt-6
            prose-h3:mb-3

            prose-p:text-gray-200
            prose-p:text-lg
            prose-p:leading-8

            prose-strong:text-white
            prose-strong:font-bold

            prose-ul:space-y-3
            prose-li:text-lg
            prose-li:text-gray-200
            prose-li:marker:text-sky-400

            prose-blockquote:bg-white/5
            prose-blockquote:border-l-4
            prose-blockquote:border-sky-400
            prose-blockquote:px-5
            prose-blockquote:py-3
            prose-blockquote:rounded-xl
          "
        >
          <ReactMarkdown>{text}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default Itinerary;