import React from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar = () => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path ? "bg-blue-600 shadow-lg shadow-blue-500/50" : "hover:bg-gray-700";

  return (
    <nav className="bg-gray-900/80 backdrop-blur-md sticky top-0 z-50 border-b border-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-black tracking-tighter bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          NLP.LAB
        </Link>
        <div className="flex space-x-2">
          {[
            { name: "Statistics", path: "/statistics" },
            { name: "Syntax", path: "/syntax" },
            { name: "POS", path: "/pos" },
            { name: "NER", path: "/ner" },
            { name: "Topics", path: "/topics" }
          ].map((link) => (
            <Link 
              key={link.path} 
              to={link.path} 
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${isActive(link.path)}`}
            >
              {link.name}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;