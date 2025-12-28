// Demo mode utilities for development and testing
export const isDemoMode = () => {
  return import.meta.env.VITE_DEMO_MODE === 'true' || false;
};

// Demo data storage
let demoUsers = [];
let demoAnalyses = [];
let currentDemoUser = null;

export const initDemoData = () => {
  // Initialize with some demo users if not already present
  if (demoUsers.length === 0) {
    demoUsers = [
      {
        id: 'demo-user-1',
        username: 'demo',
        email: 'demo@pixeltruth.com',
        plan: 'free',
        analysesUsed: 3,
        analysesLimit: 10,
        createdAt: new Date().toISOString()
      }
    ];
  }
};

export const demoAPI = {
  login: async (email, password) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    if (email === 'demo@pixeltruth.com' && password === 'demo123') {
      const user = demoUsers[0];
      currentDemoUser = user;
      return {
        success: true,
        token: 'demo-token-' + Date.now(),
        user
      };
    }
    
    throw new Error('Invalid credentials');
  },

  register: async (userData) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const newUser = {
      id: 'demo-user-' + Date.now(),
      username: userData.username,
      email: userData.email,
      plan: 'free',
      analysesUsed: 0,
      analysesLimit: 10,
      createdAt: new Date().toISOString()
    };
    
    demoUsers.push(newUser);
    currentDemoUser = newUser;
    
    return {
      success: true,
      token: 'demo-token-' + Date.now(),
      user: newUser
    };
  },

  getCurrentUser: async () => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 200));
    
    if (currentDemoUser) {
      return { user: currentDemoUser };
    }
    
    throw new Error('Not authenticated');
  },

  analyzeImage: async (imageData) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const analysis = {
      id: 'analysis-' + Date.now(),
      userId: currentDemoUser?.id,
      filename: imageData.name || 'uploaded-image.jpg',
      isAIGenerated: Math.random() > 0.5,
      confidence: Math.floor(Math.random() * 30) + 70, // 70-99%
      authenticity: Math.floor(Math.random() * 40) + 60, // 60-99%
      metadata: {
        hasExif: Math.random() > 0.3,
        dimensions: '1920x1080',
        fileSize: '2.4 MB',
        format: 'JPEG'
      },
      osintResults: {
        reverseImageSearch: Math.random() > 0.4,
        similarImages: Math.floor(Math.random() * 10),
        firstSeen: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString()
      },
      createdAt: new Date().toISOString()
    };
    
    demoAnalyses.push(analysis);
    
    if (currentDemoUser) {
      currentDemoUser.analysesUsed += 1;
    }
    
    return { analysis };
  },

  getAnalysisHistory: async () => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    
    return {
      analyses: demoAnalyses.filter(a => a.userId === currentDemoUser?.id)
    };
  },

  getAnalysis: async (id) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 200));
    
    const analysis = demoAnalyses.find(a => a.id === id);
    if (!analysis) {
      throw new Error('Analysis not found');
    }
    
    return { analysis };
  }
};