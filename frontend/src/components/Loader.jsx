import { motion } from "framer-motion";

const steps = [
  "Searching flights...",
  "Finding hotels...",
  "Checking weather...",
  "Generating AI itinerary...",
];

const Loader = () => {
  return (
    <div className="space-y-5">
      {steps.map((step, i) => (
        <motion.div
          key={i}
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{
            repeat: Infinity,
            duration: 2,
            delay: i * 0.4,
          }}
          className="bg-white/10 rounded-xl p-5"
        >
          {step}
        </motion.div>
      ))}
    </div>
  );
};

export default Loader;