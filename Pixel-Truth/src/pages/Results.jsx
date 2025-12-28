import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CheckCircle, XCircle, Clock, Camera, MapPin, Calendar, ArrowLeft, Download, Eye } from 'lucide-react';
import axios from 'axios';

const Results = () => {
  const { analysisId } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [allAnalyses, setAllAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState(null);

  // If no analysisId, show all results
  const showAllResults = !analysisId;

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (showAllResults) {
          // Fetch all analyses
          console.log('🔍 Fetching analysis history...');
          const response = await axios.get('/api/analysis/history?limit=20');
          console.log('📊 Analysis history response:', response.data);
          setAllAnalyses(response.data.analyses);
          setPagination(response.data.pagination);
        } else {
          // Fetch specific analysis
          console.log('🔍 Fetching specific analysis:', analysisId);
          const response = await axios.get(`/api/analysis/${analysisId}`);
          console.log('📊 Specific analysis response:', response.data);
          setAnalysis(response.data);
        }
      } catch (error) {
        console.error('❌ Error fetching data:', error);
        console.error('❌ Error response:', error.response?.data);
        setError(showAllResults ? 'Failed to load analysis history' : 'Failed to load analysis results');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [analysisId, showAllResults]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <XCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link to="/dashboard" className="btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  // Show all results page
  if (showAllResults) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <Link
              to="/dashboard"
              className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Link>
            
            <h1 className="text-3xl font-bold text-gray-900">All Analysis Results</h1>
            <p className="text-gray-600">View all your image analysis history</p>
          </div>

          {/* Results List */}
          {allAnalyses.length === 0 ? (
            <div className="bg-white rounded-lg shadow-md p-12 text-center">
              <Clock className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No analyses yet</h3>
              <p className="text-gray-600 mb-6">Upload your first image to get started with authenticity verification.</p>
              <Link to="/upload" className="btn-primary">
                Analyze Your First Image
              </Link>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="divide-y divide-gray-200">
                {allAnalyses.map((analysisItem) => (
                  <div key={analysisItem._id} className="p-6 hover:bg-gray-50 transition-colors duration-200">
                    <div className="flex items-center space-x-4">
                      <img
                        src={analysisItem.image_url}
                        alt="Analysis"
                        className="w-20 h-20 object-cover rounded-lg flex-shrink-0"
                      />
                      
                      <div className="flex-grow min-w-0">
                        <h3 className="text-lg font-medium text-gray-900 truncate">
                          {analysisItem.original_filename}
                        </h3>
                        <p className="text-sm text-gray-500 mb-2">
                          Analyzed on {new Date(analysisItem.created_at).toLocaleDateString()} at {new Date(analysisItem.created_at).toLocaleTimeString()}
                        </p>
                        <p className="text-sm text-gray-600">
                          Processing time: {analysisItem.processing_time}ms
                        </p>
                      </div>

                      <div className="text-center">
                        <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                          analysisItem.final_verdict.is_authentic
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {analysisItem.final_verdict.is_authentic ? (
                            <>
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Authentic
                            </>
                          ) : (
                            <>
                              <XCircle className="w-4 h-4 mr-1" />
                              AI Generated
                            </>
                          )}
                        </div>
                        <p className="text-sm text-gray-500 mt-1">
                          {(analysisItem.final_verdict.overall_confidence * 100).toFixed(1)}% confidence
                        </p>
                      </div>

                      <Link
                        to={`/results/${analysisItem._id}`}
                        className="btn-secondary flex items-center"
                      >
                        <Eye className="h-4 w-4 mr-2" />
                        View Details
                      </Link>
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination */}
              {pagination && pagination.pages > 1 && (
                <div className="bg-gray-50 px-6 py-3 border-t border-gray-200">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-gray-700">
                      Showing {((pagination.page - 1) * pagination.limit) + 1} to {Math.min(pagination.page * pagination.limit, pagination.total)} of {pagination.total} results
                    </p>
                    <div className="flex space-x-2">
                      {pagination.page > 1 && (
                        <button className="btn-secondary text-sm">Previous</button>
                      )}
                      {pagination.page < pagination.pages && (
                        <button className="btn-secondary text-sm">Next</button>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }

  // Show specific analysis (existing code)
  if (!analysis) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <XCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Not Found</h2>
          <p className="text-gray-600 mb-4">The requested analysis could not be found.</p>
          <Link to="/dashboard" className="btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const { final_verdict, ml_result, osint_result, processing_time } = analysis;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link
            to="/dashboard"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Link>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Analysis Results</h1>
              <p className="text-gray-600">{analysis.original_filename}</p>
            </div>
            <button className="btn-secondary flex items-center">
              <Download className="h-4 w-4 mr-2" />
              Export Report
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Image and Overall Result */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <img
                src={analysis.image_url}
                alt="Analyzed"
                className="w-full rounded-lg mb-4"
              />
              
              <div className="text-center">
                <div className={`inline-flex items-center px-4 py-2 rounded-full text-lg font-semibold ${
                  final_verdict.is_authentic
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {final_verdict.is_authentic ? (
                    <>
                      <CheckCircle className="w-5 h-5 mr-2" />
                      Authentic
                    </>
                  ) : (
                    <>
                      <XCircle className="w-5 h-5 mr-2" />
                      AI Generated
                    </>
                  )}
                </div>
                
                <div className="mt-4">
                  <div className="text-3xl font-bold text-gray-900">
                    {(final_verdict.overall_confidence * 100).toFixed(1)}%
                  </div>
                  <div className="text-gray-600">Confidence</div>
                </div>
              </div>
            </div>

            {/* Processing Info */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Processing Info</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Processing Time</span>
                  <span className="font-medium">{processing_time}ms</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">File Size</span>
                  <span className="font-medium">{(analysis.file_size / 1024 / 1024).toFixed(2)} MB</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Analyzed</span>
                  <span className="font-medium">
                    {new Date(analysis.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Results */}
          <div className="lg:col-span-2 space-y-6">
            {/* Overall Assessment */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Overall Assessment</h2>
              <p className="text-gray-700 leading-relaxed">
                {final_verdict.reasoning}
              </p>
            </div>

            {/* ML Analysis */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Machine Learning Analysis</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {(ml_result.confidence * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600">ML Confidence</div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className={`text-2xl font-bold ${ml_result.is_ai_generated ? 'text-red-600' : 'text-green-600'}`}>
                    {ml_result.is_ai_generated ? 'AI' : 'Real'}
                  </div>
                  <div className="text-sm text-gray-600">ML Verdict</div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {ml_result.model_version}
                  </div>
                  <div className="text-sm text-gray-600">Model Version</div>
                </div>
              </div>

              <p className="text-gray-700">
                Our advanced machine learning model analyzed the image for signs of AI generation, 
                examining pixel patterns, compression artifacts, and other technical indicators.
              </p>
            </div>

            {/* OSINT Analysis */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">OSINT Analysis</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Metadata */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Metadata Analysis</h3>
                  
                  {osint_result.has_metadata ? (
                    <div className="space-y-3">
                      {osint_result.metadata?.camera && (
                        <div className="flex items-center space-x-2">
                          <Camera className="h-4 w-4 text-gray-500" />
                          <span className="text-sm text-gray-700">{osint_result.metadata.camera}</span>
                        </div>
                      )}
                      
                      {osint_result.metadata?.timestamp && (
                        <div className="flex items-center space-x-2">
                          <Calendar className="h-4 w-4 text-gray-500" />
                          <span className="text-sm text-gray-700">
                            {new Date(osint_result.metadata.timestamp).toLocaleString()}
                          </span>
                        </div>
                      )}
                      
                      {osint_result.metadata?.location && (
                        <div className="flex items-center space-x-2">
                          <MapPin className="h-4 w-4 text-gray-500" />
                          <span className="text-sm text-gray-700">
                            {osint_result.metadata.location.latitude.toFixed(4)}, {osint_result.metadata.location.longitude.toFixed(4)}
                          </span>
                        </div>
                      )}
                      
                      {osint_result.metadata?.dimensions && (
                        <div className="text-sm text-gray-700">
                          Dimensions: {osint_result.metadata.dimensions.width} × {osint_result.metadata.dimensions.height}
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No EXIF metadata found</p>
                  )}
                </div>

                {/* Reverse Image Search */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Reverse Image Search</h3>
                  
                  {osint_result.reverse_image_search.found ? (
                    <div className="space-y-2">
                      <p className="text-sm text-gray-700">
                        Found {osint_result.reverse_image_search.sources.length} similar images online
                      </p>
                      {osint_result.reverse_image_search.sources.slice(0, 3).map((source, index) => (
                        <div key={index} className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                          <div>Similarity: {(source.similarity * 100).toFixed(1)}%</div>
                          <div>First seen: {new Date(source.first_seen).toLocaleDateString()}</div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No similar images found online</p>
                  )}
                </div>
              </div>

              {/* Authenticity Factors */}
              <div className="mt-6">
                <h3 className="font-semibold text-gray-900 mb-3">Authenticity Factors</h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium">Authenticity Score</span>
                    <span className="text-lg font-bold text-blue-600">
                      {(osint_result.authenticity.score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="bg-gray-200 rounded-full h-2 mb-3">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${osint_result.authenticity.score * 100}%` }}
                    ></div>
                  </div>
                  <ul className="text-sm text-gray-700 space-y-1">
                    {osint_result.authenticity.factors.map((factor, index) => (
                      <li key={index} className="flex items-center">
                        <div className="w-2 h-2 bg-blue-600 rounded-full mr-2 flex-shrink-0"></div>
                        {factor}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;