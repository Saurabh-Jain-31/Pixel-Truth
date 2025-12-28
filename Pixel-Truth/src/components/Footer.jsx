import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Mail, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo and About */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <Shield className="h-8 w-8 text-blue-400" />
              <span className="text-xl font-bold">Pixel Truth</span>
            </div>
            <p className="text-gray-300 mb-4 max-w-md">
              Advanced image authenticity verification platform using Machine Learning 
              and OSINT analysis to detect AI-generated and manipulated images.
            </p>
            <div className="text-sm text-gray-400">
              <p className="mb-2">Made by Saurabh Jain, Ajay Meena and Shiva Gupta</p>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-300 hover:text-blue-400 transition-colors duration-200">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-300 hover:text-blue-400 transition-colors duration-200">
                  About
                </Link>
              </li>
              <li>
                <Link to="/features" className="text-gray-300 hover:text-blue-400 transition-colors duration-200">
                  Features
                </Link>
              </li>
              <li>
                <Link to="/plans" className="text-gray-300 hover:text-blue-400 transition-colors duration-200">
                  Plans
                </Link>
              </li>
              <li>
                <Link to="/upload" className="text-gray-300 hover:text-blue-400 transition-colors duration-200">
                  Upload / Analyze
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Mail className="h-4 w-4 text-blue-400" />
                <span className="text-gray-300">support@pixeltruth.com</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="h-4 w-4 text-blue-400" />
                <span className="text-gray-300">
                  Tech Innovation Hub<br />
                  Digital Security Center<br />
                  India
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-400 text-sm">
              © 2024 Pixel Truth. All rights reserved.
            </div>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <Link to="/privacy" className="text-gray-400 hover:text-blue-400 text-sm transition-colors duration-200">
                Privacy Policy
              </Link>
              <Link to="/terms" className="text-gray-400 hover:text-blue-400 text-sm transition-colors duration-200">
                Terms of Service
              </Link>
              <Link to="/contact" className="text-gray-400 hover:text-blue-400 text-sm transition-colors duration-200">
                Contact Us
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;