import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CheckCircle, XCircle, Clock, Upload, ArrowLeft, Eye } from 'lucide-react';
import axios from 'axios';

const Results = () => {
  const { analysisId } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [allAnalyses, setAllAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
          setAllAnalyses(response.data.analyses || []);
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
              <Upload className="h-16 w-16 text-gray-400 mx-auto mb-4" />
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
                  <div key={analysisItem.id} className="p-6 hover:bg-gray-50 transition-colors duration-200">
                    <div className="flex items-center space-x-4">
                      <div className="w-20 h-20 bg-gray-200 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Upload className="h-8 w-8 text-gray-400" />
                      </div>
                      
                      <div className="flex-grow min-w-0">
                        <h3 className="text-lg font-medium text-gray-900 truncate">
                          {analysisItem.filename || 'Unknown file'}
                        </h3>
                        <p className="text-sm text-gray-500 mb-2">
                          Analyzed on {new Date(analysisItem.created_at).toLocaleDateString()} at {new Date(analysisItem.created_at).toLocaleTimeString()}
                        </p>
                        <p className="text-sm text-gray-600">
                          Type: {analysisItem.type || 'image'}
                        </p>
                      </div>

                      <div className="text-center">
                        <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                          analysisItem.prediction === 'authentic'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {analysisItem.prediction === 'authentic' ? (
                            <>
                              <CheckCircle className="w-4 h-4 mr-1" />
                              Authentic
                            </>
                          ) : (
                            <>
                              <XCircle className="w-4 h-4 mr-1" />
                              {analysisItem.prediction === 'ai_generated' ? 'AI Generated' : 'Manipulated'}
                            </>
                          )}
                        </div>
                        <p className="text-sm text-gray-500 mt-1">
                          {((analysisItem.confidence_score || 0) * 100).toFixed(1)}% confidence
                        </p>
                      </div>

                      <Link
                        to={`/results/${analysisItem.id}`}
                        className="btn-secondary flex items-center"
                      >
                        <Eye className="h-4 w-4 mr-2" />
                        View Details
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Show specific analysis
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

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link
            to="/dashboard"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Link>
          
          <h1 className="text-3xl font-bold text-gray-900">Analysis Results</h1>
          <p className="text-gray-600">{analysis.original_filename}</p>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="text-center mb-8">
            <div className={`inline-flex items-center px-6 py-3 rounded-full text-xl font-semibold ${
              analysis.final_verdict?.is_authentic
                ? 'bg-green-100 text-green-800'
                : 'bg-red-100 text-red-800'
            }`}>
              {analysis.final_verdict?.is_authentic ? (
                <>
                  <CheckCircle className="w-6 h-6 mr-2" />
                  Authentic
                </>
              ) : (
                <>
                  <XCircle className="w-6 h-6 mr-2" />
                  AI Generated
                </>
              )}
            </div>
            
            <div className="mt-4">
              <div className="text-4xl font-bold text-gray-900">
                {((analysis.final_verdict?.overall_confidence || 0) * 100).toFixed(1)}%
              </div>
              <div className="text-gray-600">Confidence</div>
            </div>
          </div>

          {/* Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Analysis Details</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Processing Time:</span>
                  <span className="font-medium">{analysis.processing_time}ms</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">File Size:</span>
                  <span className="font-medium">{(analysis.file_size / 1024 / 1024).toFixed(2)} MB</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Analyzed:</span>
                  <span className="font-medium">{new Date(analysis.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Assessment</h3>
              <p className="text-gray-700 text-sm">
                {analysis.final_verdict?.reasoning || 'Analysis completed successfully.'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;