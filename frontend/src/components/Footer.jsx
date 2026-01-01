
// Footer.jsx
import React from "react";

const Footer = () => (
    <footer className="py-12 border-t border-slate-100 bg-white">
    <div className="container mx-auto px-4 text-center">
      <p className="text-slate-400 text-sm font-medium">
        &copy; {new Date().getFullYear()} NLP Studio • Built By fares samer
      </p>
    </div>
  </footer>
);

export default Footer;