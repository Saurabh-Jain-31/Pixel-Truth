import React from 'react';
import { Shield, Users, Target, Award } from 'lucide-react';

const About = () => {
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

      {/* Team Section */}
      <section className="bg-gray-50 py-20">
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