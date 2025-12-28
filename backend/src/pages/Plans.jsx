import React from 'react';
import { Check, Star } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Plans = () => {
  const { user, isAuthenticated } = useAuth();

  const handlePlanClick = (e, planName) => {
    if (!isAuthenticated) {
      // Let the Link handle navigation to register
      return;
    }
    
    if (user?.plan === planName.toLowerCase()) {
      // Already on this plan, prevent navigation
      e.preventDefault();
      return;
    }
    
    // Prevent navigation and show upgrade message
    e.preventDefault();
    alert(`Plan upgrade to ${planName} will be available soon! This would integrate with Stripe/PayPal for payment processing.`);
  };

  const plans = [
    {
      name: 'Free',
      price: '$0',
      period: '/month',
      description: 'Perfect for trying out our service',
      features: [
        '10 image analyses per month',
        'Basic ML detection',
        'OSINT metadata analysis',
        'Standard support',
        'Web dashboard access'
      ],
      buttonText: isAuthenticated ? 'Current Plan' : 'Get Started',
      buttonClass: isAuthenticated && user?.plan === 'free' ? 'btn-secondary opacity-50 cursor-not-allowed' : 'btn-secondary',
      popular: false,
      isCurrentPlan: isAuthenticated && user?.plan === 'free'
    },
    {
      name: 'Basic',
      price: '$9.99',
      period: '/month',
      description: 'Great for regular users and small teams',
      features: [
        '100 image analyses per month',
        'Advanced ML detection',
        'Full OSINT analysis',
        'Priority support',
        'API access',
        'Detailed reports',
        'Export capabilities'
      ],
      buttonText: isAuthenticated ? (user?.plan === 'basic' ? 'Current Plan' : 'Upgrade to Basic') : 'Choose Basic',
      buttonClass: isAuthenticated && user?.plan === 'basic' ? 'btn-primary opacity-50 cursor-not-allowed' : 'btn-primary',
      popular: true,
      isCurrentPlan: isAuthenticated && user?.plan === 'basic'
    },
    {
      name: 'Pro',
      price: '$29.99',
      period: '/month',
      description: 'For professionals and organizations',
      features: [
        '1000 image analyses per month',
        'Premium ML models',
        'Advanced OSINT features',
        '24/7 priority support',
        'Full API access',
        'Custom integrations',
        'Bulk analysis',
        'Team management',
        'White-label options'
      ],
      buttonText: isAuthenticated ? (user?.plan === 'pro' ? 'Current Plan' : 'Upgrade to Pro') : 'Choose Pro',
      buttonClass: isAuthenticated && user?.plan === 'pro' ? 'btn-primary opacity-50 cursor-not-allowed' : 'btn-primary',
      popular: false,
      isCurrentPlan: isAuthenticated && user?.plan === 'pro'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Select the perfect plan for your image verification needs. 
            All plans include our advanced ML detection and OSINT analysis.
          </p>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <div
                key={index}
                className={`bg-white rounded-lg shadow-lg overflow-hidden ${
                  plan.popular ? 'ring-2 ring-blue-600 relative' : ''
                }`}
              >
                {plan.popular && (
                  <div className="absolute top-0 right-0 bg-blue-600 text-white px-4 py-1 text-sm font-medium rounded-bl-lg">
                    <Star className="inline w-4 h-4 mr-1" />
                    Most Popular
                  </div>
                )}
                
                <div className="p-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    {plan.name}
                  </h3>
                  <p className="text-gray-600 mb-6">
                    {plan.description}
                  </p>
                  
                  <div className="mb-6">
                    <span className="text-4xl font-bold text-gray-900">
                      {plan.price}
                    </span>
                    <span className="text-gray-600">
                      {plan.period}
                    </span>
                  </div>

                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center">
                        <Check className="h-5 w-5 text-green-600 mr-3 flex-shrink-0" />
                        <span className="text-gray-700">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  {plan.isCurrentPlan ? (
                    <button
                      disabled
                      className={`w-full ${plan.buttonClass} text-center block`}
                    >
                      {plan.buttonText}
                    </button>
                  ) : (
                    <Link
                      to={isAuthenticated ? "#" : "/register"}
                      onClick={(e) => handlePlanClick(e, plan.name)}
                      className={`w-full ${plan.buttonClass} text-center block`}
                    >
                      {plan.buttonText}
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="bg-white py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600">
              Everything you need to know about our plans and pricing
            </p>
          </div>

          <div className="space-y-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Can I upgrade or downgrade my plan anytime?
              </h3>
              <p className="text-gray-600">
                Yes, you can change your plan at any time. Changes take effect immediately, 
                and we'll prorate any billing adjustments.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                What happens if I exceed my monthly limit?
              </h3>
              <p className="text-gray-600">
                If you reach your monthly analysis limit, you'll need to upgrade your plan 
                or wait until the next billing cycle. We'll notify you when you're approaching your limit.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Do you offer refunds?
              </h3>
              <p className="text-gray-600">
                We offer a 30-day money-back guarantee for all paid plans. 
                If you're not satisfied, contact us for a full refund.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Is there an enterprise plan available?
              </h3>
              <p className="text-gray-600">
                Yes, we offer custom enterprise solutions with unlimited analyses, 
                dedicated support, and custom integrations. Contact us for pricing.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                How accurate is the detection?
              </h3>
              <p className="text-gray-600">
                Our system achieves 99.2% accuracy in detecting AI-generated images, 
                combining advanced machine learning with comprehensive OSINT analysis.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of users who trust Pixel Truth for image authenticity verification
          </p>
          <Link
            to="/register"
            className="bg-white text-blue-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors duration-200"
          >
            Start Free Trial
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Plans;