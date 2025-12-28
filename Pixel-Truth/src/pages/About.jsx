import React from 'react';
import { Shield, Users, Target, Award, Calendar, Code, Database, Brain, Globe, Rocket } from 'lucide-react';

const About = () => {
  const timelineSteps = [
    {
      phase: "Idea & Research",
      period: "2025",
      description: "Conceptualized the need for AI image detection and researched existing solutions",
      icon: Brain,
      color: "blue",
      emoji: "💡"
    },
    {
      phase: "Dataset Collection",
      period: "2025", 
      description: "Gathered comprehensive datasets of AI-generated and authentic images",
      icon: Database,
      color: "green",
      emoji: "📊"
    },
    {
      phase: "ML Model Training",
      period: "2025",
      description: "Developed and trained advanced machine learning models for detection",
      icon: Brain,
      color: "purple",
      emoji: "🤖"
    },
    {
      phase: "OSINT Integration",
      period: "2025",
      description: "Integrated Open Source Intelligence tools for metadata analysis",
      icon: Globe,
      color: "orange",
      emoji: "🔍"
    },
    {
      phase: "Frontend & Backend Development",
      period: "2025",
      description: "Built full-stack application with React frontend and FastAPI backend",
      icon: Code,
      color: "indigo",
      emoji: "⚙️"
    },
    {
      phase: "Deployment & Testing",
      period: "2025",
      description: "Deployed the platform and conducted extensive testing for reliability",
      icon: Rocket,
      color: "red",
      emoji: "🚀"
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            About Pixel Truth
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            We're on a mission to combat the spread of AI-generated and manipulated images 
            through cutting-edge technology and innovative solutions.
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
              <p className="text-lg text-gray-600 mb-6">
                In an era where AI-generated content is becoming increasingly sophisticated, 
                we believe in the fundamental right to truth and authenticity. Pixel Truth 
                was created to empower individuals, organizations, and institutions with the 
                tools they need to verify image authenticity.
              </p>
              <p className="text-lg text-gray-600">
                Our advanced machine learning algorithms combined with comprehensive OSINT 
                analysis provide unparalleled accuracy in detecting manipulated and 
                AI-generated images.
              </p>
            </div>
            <div className="bg-blue-50 rounded-lg p-8">
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">99.2%</div>
                  <div className="text-gray-600">Accuracy Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">1M+</div>
                  <div className="text-gray-600">Images Analyzed</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">50K+</div>
                  <div className="text-gray-600">Active Users</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600 mb-2">&lt;2s</div>
                  <div className="text-gray-600">Analysis Time</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Development Timeline Section */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Development Timeline</h2>
            <p className="text-xl text-gray-600">
              How we built Pixel Truth from concept to deployment
            </p>
          </div>

          {/* Timeline Container with Exact Positioning */}
          <div className="relative" style={{ minHeight: '1600px' }}>
            
            {/* Timeline Steps - Each positioned exactly */}
            {timelineSteps.map((step, index) => {
              const IconComponent = step.icon;
              const isEven = index % 2 === 0;
              const progressPercentage = Math.round(((index + 1) / timelineSteps.length) * 100);
              
              // Exact positioning for each step (256px spacing)
              const topPosition = 32 + (index * 256);
              
              const colorClasses = {
                blue: { 
                  node: 'bg-blue-500', 
                  iconBg: 'bg-blue-100', 
                  iconText: 'text-blue-600',
                  border: 'border-blue-500',
                  badge: 'bg-blue-100 text-blue-800',
                  progress: 'bg-blue-500'
                },
                green: { 
                  node: 'bg-green-500', 
                  iconBg: 'bg-green-100', 
                  iconText: 'text-green-600',
                  border: 'border-green-500',
                  badge: 'bg-green-100 text-green-800',
                  progress: 'bg-green-500'
                },
                purple: { 
                  node: 'bg-purple-500', 
                  iconBg: 'bg-purple-100', 
                  iconText: 'text-purple-600',
                  border: 'border-purple-500',
                  badge: 'bg-purple-100 text-purple-800',
                  progress: 'bg-purple-500'
                },
                orange: { 
                  node: 'bg-orange-500', 
                  iconBg: 'bg-orange-100', 
                  iconText: 'text-orange-600',
                  border: 'border-orange-500',
                  badge: 'bg-orange-100 text-orange-800',
                  progress: 'bg-orange-500'
                },
                indigo: { 
                  node: 'bg-indigo-500', 
                  iconBg: 'bg-indigo-100', 
                  iconText: 'text-indigo-600',
                  border: 'border-indigo-500',
                  badge: 'bg-indigo-100 text-indigo-800',
                  progress: 'bg-indigo-500'
                },
                red: { 
                  node: 'bg-red-500', 
                  iconBg: 'bg-red-100', 
                  iconText: 'text-red-600',
                  border: 'border-red-500',
                  badge: 'bg-red-100 text-red-800',
                  progress: 'bg-red-500'
                }
              };
              
              const colors = colorClasses[step.color];
              
              return (
                <div key={index} className="absolute w-full" style={{ top: `${topPosition}px` }}>
                  <div className={`relative flex items-center ${isEven ? 'justify-start' : 'justify-end'}`}>
                    {/* Timeline Node - Positioned at exact center */}
                    <div className="absolute left-1/2 transform -translate-x-1/2 z-30">
                      <div className={`w-12 h-12 ${colors.node} rounded-full border-4 border-white shadow-2xl relative`}>
                        <div className="absolute -top-16 left-1/2 transform -translate-x-1/2">
                          <span className="text-5xl filter drop-shadow-2xl">{step.emoji}</span>
                        </div>
                      </div>
                    </div>
                    
                    {/* Content Card */}
                    <div className={`w-5/12 ${isEven ? 'pr-24' : 'pl-24'}`}>
                      <div className={`bg-white rounded-2xl shadow-2xl p-8 border-l-4 ${colors.border} hover:shadow-3xl transition-all duration-300 transform hover:scale-105`}>
                        <div className="flex items-center mb-6">
                          <div className={`${colors.iconBg} rounded-full p-4 mr-4 shadow-lg`}>
                            <IconComponent className={`h-8 w-8 ${colors.iconText}`} />
                          </div>
                          <div>
                            <h3 className="text-2xl font-bold text-gray-900 mb-2">{step.phase}</h3>
                            <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold ${colors.badge}`}>
                              <Calendar className="h-4 w-4 mr-2" />
                              {step.period}
                            </div>
                          </div>
                        </div>
                        <p className="text-gray-700 leading-relaxed mb-6 text-lg">{step.description}</p>
                        
                        <div className="mt-6 flex items-center">
                          <div className="flex-1 bg-gray-300 rounded-full h-4 overflow-hidden shadow-inner">
                            <div 
                              className={`${colors.progress} h-full rounded-full transition-all duration-2000 ease-out shadow-sm`}
                              style={{ width: `${progressPercentage}%` }}
                            ></div>
                          </div>
                          <span className={`ml-4 text-lg font-bold ${colors.iconText} bg-white px-3 py-1 rounded-full shadow-md`}>
                            {progressPercentage}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}

            {/* Perfect Zigzag Line - Positioned to Connect Exact Node Centers */}
            <div className="absolute left-1/2 transform -translate-x-1/2 w-20 h-full z-10">
              <svg 
                className="w-full h-full" 
                viewBox="0 0 80 1600" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
                style={{ minHeight: '1600px', width: '80px' }}
                preserveAspectRatio="xMidYMid meet"
              >
                {/* PERFECTLY Aligned Path - Final Precision Adjustment */}
                <path 
                  d="M40 168 Q60 284 40 424 Q20 564 40 680 Q60 820 40 936 Q20 1076 40 1192 Q60 1332 40 1448"
                  stroke="#1E40AF" 
                  strokeWidth="8" 
                  fill="none"
                  opacity="1"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                
                <path 
                  d="M40 168 Q60 284 40 424 Q20 564 40 680 Q60 820 40 936 Q20 1076 40 1192 Q60 1332 40 1448"
                  stroke="url(#perfectGradient)" 
                  strokeWidth="6" 
                  fill="none"
                  opacity="0.9"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                
                <path 
                  d="M40 168 Q60 284 40 424 Q20 564 40 680 Q60 820 40 936 Q20 1076 40 1192 Q60 1332 40 1448"
                  stroke="#3B82F6" 
                  strokeWidth="2" 
                  fill="none"
                  opacity="0.6"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  filter="url(#perfectGlow)"
                />
                
                {/* Connection Indicators at Pixel-Perfect Centers */}
                <circle cx="40" cy="168" r="4" fill="#3B82F6" opacity="0.8" stroke="#FFF" strokeWidth="1" />
                <circle cx="40" cy="424" r="4" fill="#10B981" opacity="0.8" stroke="#FFF" strokeWidth="1" />
                <circle cx="40" cy="680" r="4" fill="#8B5CF6" opacity="0.8" stroke="#FFF" strokeWidth="1" />
                <circle cx="40" cy="936" r="4" fill="#F59E0B" opacity="0.8" stroke="#FFF" strokeWidth="1" />
                <circle cx="40" cy="1192" r="4" fill="#6366F1" opacity="0.8" stroke="#FFF" strokeWidth="1" />
                <circle cx="40" cy="1448" r="4" fill="#EF4444" opacity="0.8" stroke="#FFF" strokeWidth="1" />
                
                {/* Animated dot */}
                <circle r="3" fill="#3B82F6" opacity="0.8">
                  <animateMotion dur="8s" repeatCount="indefinite">
                    <mpath href="#perfectPath"/>
                  </animateMotion>
                </circle>
                
                <path 
                  id="perfectPath"
                  d="M40 168 Q60 284 40 424 Q20 564 40 680 Q60 820 40 936 Q20 1076 40 1192 Q60 1332 40 1448"
                  fill="none"
                  opacity="0"
                />
                
                <defs>
                  <linearGradient id="perfectGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#3B82F6" />
                    <stop offset="16.67%" stopColor="#10B981" />
                    <stop offset="33.33%" stopColor="#8B5CF6" />
                    <stop offset="50%" stopColor="#F59E0B" />
                    <stop offset="66.67%" stopColor="#6366F1" />
                    <stop offset="83.33%" stopColor="#EF4444" />
                    <stop offset="100%" stopColor="#EC4899" />
                  </linearGradient>
                  <filter id="perfectGlow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge> 
                      <feMergeNode in="coloredBlur"/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>
                </defs>
              </svg>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Meet Our Team</h2>
            <p className="text-xl text-gray-600">
              Passionate developers and researchers dedicated to digital truth
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-4">
                <Users className="h-12 w-12 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Saurabh Jain</h3>
              <p className="text-gray-600 mb-2">Lead Developer & ML Engineer</p>
              <p className="text-sm text-gray-500">
                Specializes in machine learning and computer vision algorithms
              </p>
            </div>

            <div className="text-center">
              <div className="bg-green-100 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-4">
                <Shield className="h-12 w-12 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Ajay Meena</h3>
              <p className="text-gray-600 mb-2">Security & OSINT Specialist</p>
              <p className="text-sm text-gray-500">
                Expert in digital forensics and open-source intelligence
              </p>
            </div>

            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-4">
                <Target className="h-12 w-12 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Shiva Gupta</h3>
              <p className="text-gray-600 mb-2">Full-Stack Developer</p>
              <p className="text-sm text-gray-500">
                Focuses on user experience and system architecture
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Values</h2>
            <p className="text-xl text-gray-600">
              The principles that guide everything we do
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Accuracy</h3>
              <p className="text-gray-600 text-sm">
                We strive for the highest precision in our detection algorithms
              </p>
            </div>

            <div className="text-center">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Transparency</h3>
              <p className="text-gray-600 text-sm">
                Clear explanations of our methods and results
              </p>
            </div>

            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Target className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Innovation</h3>
              <p className="text-gray-600 text-sm">
                Continuously improving our technology and methods
              </p>
            </div>

            <div className="text-center">
              <div className="bg-orange-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Award className="h-8 w-8 text-orange-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Integrity</h3>
              <p className="text-gray-600 text-sm">
                Committed to ethical practices and user privacy
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;