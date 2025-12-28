import React from 'react';
import { Shield, Zap, Eye, Brain, Search, BarChart3, Lock, Globe } from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: Brain,
      title: 'Advanced ML Detection',
      description: 'State-of-the-art neural networks trained on millions of images to detect AI-generated content with 99.2% accuracy.',
      color: 'blue'
    },
    {
      icon: Search,
      title: 'OSINT Analysis',
      description: 'Comprehensive metadata extraction and reverse image search to verify image authenticity and origin.',
      color: 'green'
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Get results in under 2 seconds with our optimized analysis pipeline and cloud infrastructure.',
      color: 'yellow'
    },
    {
      icon: BarChart3,
      title: 'Detailed Reports',
      description: 'Comprehensive analysis reports with confidence scores, reasoning, and technical details.',
      color: 'purple'
    },
    {
      icon: Lock,
      title: 'Secure & Private',
      description: 'Your images are processed securely and deleted after analysis. We never store your content.',
      color: 'red'
    },
    {
      icon: Globe,
      title: 'API Access',
      description: 'Integrate our detection capabilities into your applications with our developer-friendly API.',
      color: 'indigo'
    }
  ];

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-100 text-blue-600',
      green: 'bg-green-100 text-green-600',
      yellow: 'bg-yellow-100 text-yellow-600',
      purple: 'bg-purple-100 text-purple-600',
      red: 'bg-red-100 text-red-600',
      indigo: 'bg-indigo-100 text-indigo-600'
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Powerful Features for Image Verification
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Discover the advanced capabilities that make Pixel Truth the most accurate 
            and reliable image authenticity verification platform.
          </p>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md p-8 hover:shadow-lg transition-shadow duration-300">
                <div className={`rounded-full w-16 h-16 flex items-center justify-center mb-6 ${getColorClasses(feature.color)}`}>
                  <feature.icon className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              How Our Analysis Works
            </h2>
            <p className="text-xl text-gray-600">
              A comprehensive multi-step process for accurate image verification
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">ML Detection Pipeline</h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-4">
                  <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    1
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Image Preprocessing</h4>
                    <p className="text-gray-600">Normalize and prepare the image for analysis</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    2
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Feature Extraction</h4>
                    <p className="text-gray-600">Extract key visual features using deep learning</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    3
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">AI Detection</h4>
                    <p className="text-gray-600">Classify image as authentic or AI-generated</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    4
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Confidence Scoring</h4>
                    <p className="text-gray-600">Generate confidence score for the prediction</p>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">OSINT Analysis</h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-4">
                  <div className="bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    1
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Metadata Extraction</h4>
                    <p className="text-gray-600">Extract EXIF data, camera info, and timestamps</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    2
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Reverse Image Search</h4>
                    <p className="text-gray-600">Search for similar images across the web</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    3
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Authenticity Factors</h4>
                    <p className="text-gray-600">Analyze various authenticity indicators</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold flex-shrink-0 mt-1">
                    4
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">Final Verdict</h4>
                    <p className="text-gray-600">Combine ML and OSINT results for final assessment</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Specs */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Technical Specifications
            </h2>
            <p className="text-xl text-gray-600">
              Built with cutting-edge technology for maximum performance
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">99.2%</div>
              <div className="text-gray-600">Detection Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">&lt;2s</div>
              <div className="text-gray-600">Analysis Time</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">10MB</div>
              <div className="text-gray-600">Max File Size</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-600 mb-2">5+</div>
              <div className="text-gray-600">Image Formats</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Features;