import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import { Upload as UploadIcon, Image, AlertCircle, Loader, CheckCircle } from 'lucide-react';
import { toast } from 'react-toastify';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const Upload = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const navigate = useNavigate();
  const { user, updateUser } = useAuth();

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(progress);
        },
      });

      setUploadedFile({
        ...response.data,
        file: file,
        preview: URL.createObjectURL(file)
      });
      
      toast.success('Image uploaded successfully!');
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Upload failed');
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
    },
    multiple: false,
    disabled: isUploading || isAnalyzing
  });

  const handleAnalyze = async () => {
    if (!uploadedFile) return;

    // Check if user has remaining analyses
    if (user.analysis_count >= user.monthly_analysis_limit) {
      toast.error('You have reached your monthly analysis limit. Please upgrade your plan.');
      navigate('/plans');
      return;
    }

    setIsAnalyzing(true);

    try {
      const formData = new FormData();
      formData.append('filename', uploadedFile.filename);
      formData.append('original_name', uploadedFile.original_name);

      const response = await axios.post('/api/analysis/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Update user's remaining analyses
      updateUser({
        analysis_count: user.analysis_count + 1
      });

      toast.success('Analysis completed!');
      navigate(`/results/${response.data.analysis_id}`);
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.detail || 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const removeFile = () => {
    if (uploadedFile?.preview) {
      URL.revokeObjectURL(uploadedFile.preview);
    }
    setUploadedFile(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Upload & Analyze Image
          </h1>
          <p className="text-lg text-gray-600">
            Upload an image to verify its authenticity using our advanced AI detection system
          </p>
        </div>

        {/* User Plan Info */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                Current Plan: {user?.plan?.toUpperCase()}
              </h3>
              <p className="text-gray-600">
                Analyses used: {user?.analysis_count || 0} / {user?.monthly_analysis_limit || 10}
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-blue-600">
                {(user?.monthly_analysis_limit || 10) - (user?.analysis_count || 0)}
              </div>
              <div className="text-sm text-gray-500">Remaining</div>
            </div>
          </div>
          <div className="mt-4">
            <div className="bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{
                  width: `${((user?.analysis_count || 0) / (user?.monthly_analysis_limit || 10)) * 100}%`
                }}
              ></div>
            </div>
          </div>
        </div>

        {/* Upload Area */}
        <div className="bg-white rounded-lg shadow-md p-8">
          {!uploadedFile ? (
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors duration-200 ${
                isDragActive
                  ? 'border-blue-400 bg-blue-50'
                  : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
              } ${(isUploading || isAnalyzing) ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <input {...getInputProps()} />
              
              {isUploading ? (
                <div className="space-y-4">
                  <Loader className="h-12 w-12 text-blue-600 mx-auto animate-spin" />
                  <div>
                    <p className="text-lg font-medium text-gray-900">Uploading...</p>
                    <div className="mt-2 bg-gray-200 rounded-full h-2 max-w-xs mx-auto">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                    <p className="text-sm text-gray-500 mt-1">{uploadProgress}%</p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <UploadIcon className="h-12 w-12 text-gray-400 mx-auto" />
                  <div>
                    <p className="text-lg font-medium text-gray-900">
                      {isDragActive ? 'Drop the image here' : 'Drag & drop an image here'}
                    </p>
                    <p className="text-gray-500">or click to select a file</p>
                  </div>
                  <div className="text-sm text-gray-400">
                    <p>Supported formats: JPEG, PNG, GIF, BMP, WebP</p>
                    <p>Maximum file size: 10MB</p>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-6">
              {/* Uploaded Image Preview */}
              <div className="flex items-start space-x-6">
                <div className="flex-shrink-0">
                  <img
                    src={uploadedFile.preview}
                    alt="Uploaded"
                    className="w-32 h-32 object-cover rounded-lg border"
                  />
                </div>
                <div className="flex-grow">
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    {uploadedFile.original_name}
                  </h3>
                  <div className="text-sm text-gray-500 space-y-1">
                    <p>Size: {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                    <p>Type: {uploadedFile.mimetype}</p>
                  </div>
                  <div className="mt-4 flex space-x-3">
                    <button
                      onClick={handleAnalyze}
                      disabled={isAnalyzing}
                      className="btn-primary inline-flex items-center"
                    >
                      {isAnalyzing ? (
                        <>
                          <Loader className="animate-spin -ml-1 mr-2 h-4 w-4" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <CheckCircle className="-ml-1 mr-2 h-4 w-4" />
                          Analyze Image
                        </>
                      )}
                    </button>
                    <button
                      onClick={removeFile}
                      disabled={isAnalyzing}
                      className="btn-secondary"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>

              {/* Analysis Status */}
              {isAnalyzing && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center">
                    <Loader className="animate-spin h-5 w-5 text-blue-600 mr-3" />
                    <div>
                      <p className="text-blue-800 font-medium">Analyzing image...</p>
                      <p className="text-blue-600 text-sm">
                        Running ML detection and OSINT analysis. This may take a few seconds.
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Info Section */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-start">
            <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
            <div>
              <h3 className="text-sm font-medium text-blue-800 mb-1">
                How our analysis works
              </h3>
              <div className="text-sm text-blue-700 space-y-1">
                <p>• <strong>ML Detection:</strong> Advanced neural networks trained to identify AI-generated content</p>
                <p>• <strong>OSINT Analysis:</strong> Metadata extraction and reverse image search verification</p>
                <p>• <strong>Combined Verdict:</strong> Weighted scoring system for final authenticity assessment</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;