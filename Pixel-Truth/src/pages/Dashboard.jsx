import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BarChart3, Upload, Clock, CheckCircle, XCircle, Eye } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [recentAnalyses, setRecentAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsResponse, historyResponse] = await Promise.all([
          axios.get('/api/user/stats'),
          axios.get('/api/analysis/history?limit=5')
        ]);

        setStats(statsResponse.data);
        setRecentAnalyses(historyResponse.data.analyses);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome back, {user?.username}!</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="bg-blue-100 rounded-full p-3">
                <BarChart3 className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Analyses</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.total_analyses || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="bg-green-100 rounded-full p-3">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Authentic Images</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.authentic_images || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="bg-red-100 rounded-full p-3">
                <XCircle className="h-6 w-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">AI Generated</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.ai_generated_images || 0}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="bg-purple-100 rounded-full p-3">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">This Month</p>
                <p className="text-2xl font-bold text-gray-900">{stats?.monthly_analyses_used || 0}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Plan Status */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Plan Status</h2>
              
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Current Plan</span>
                    <span className="text-sm font-bold text-blue-600 uppercase">
                      {user?.plan || 'FREE'}
                    </span>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Monthly Usage</span>
                    <span className="text-sm text-gray-600">
                      {stats?.monthly_analyses_used || 0} / {stats?.monthly_limit || 10}
                    </span>
                  </div>
                  <div className="bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{
                        width: `${((stats?.monthly_analyses_used || 0) / (stats?.monthly_limit || 10)) * 100}%`
                      }}
                    ></div>
                  </div>
                </div>

                <div className="pt-4 border-t">
                  <p className="text-sm text-gray-600 mb-3">
                    Remaining analyses: {stats?.remaining_analyses || 0}
                  </p>
                  <Link
                    to="/plans"
                    className="w-full btn-primary text-center block"
                  >
                    Upgrade Plan
                  </Link>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-md p-6 mt-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
              
              <div className="space-y-3">
                <Link
                  to="/upload"
                  className="w-full btn-primary flex items-center justify-center"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Analyze New Image
                </Link>
                
                <Link
                  to="/results"
                  className="w-full btn-secondary flex items-center justify-center"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  View All Results
                </Link>
              </div>
            </div>
          </div>

          {/* Recent Analyses */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-lg font-semibold text-gray-900">Recent Analyses</h2>
                <Link
                  to="/results"
                  className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  View All
                </Link>
              </div>

              {recentAnalyses.length === 0 ? (
                <div className="text-center py-8">
                  <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500 mb-4">No analyses yet</p>
                  <Link to="/upload" className="btn-primary">
                    Analyze Your First Image
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {recentAnalyses.map((analysis) => (
                    <div
                      key={analysis._id}
                      className="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-200"
                    >
                      <img
                        src={analysis.image_url}
                        alt="Analysis"
                        className="w-16 h-16 object-cover rounded-lg"
                      />
                      
                      <div className="flex-grow">
                        <h3 className="font-medium text-gray-900 truncate">
                          {analysis.original_filename}
                        </h3>
                        <p className="text-sm text-gray-500">
                          {new Date(analysis.created_at).toLocaleDateString()}
                        </p>
                      </div>

                      <div className="text-right">
                        <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          analysis.final_verdict.is_authentic
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {analysis.final_verdict.is_authentic ? (
                            <>
                              <CheckCircle className="w-3 h-3 mr-1" />
                              Authentic
                            </>
                          ) : (
                            <>
                              <XCircle className="w-3 h-3 mr-1" />
                              AI Generated
                            </>
                          )}
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          {(analysis.final_verdict.overall_confidence * 100).toFixed(1)}% confidence
                        </p>
                      </div>

                      <Link
                        to={`/results/${analysis._id}`}
                        className="text-blue-600 hover:text-blue-700"
                      >
                        <Eye className="h-5 w-5" />
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;