import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  HeartIcon,
  GlobeAmericasIcon,
  AcademicCapIcon,
  TrophyIcon,
} from '@heroicons/react/24/outline';

const Home: React.FC = () => {
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: HeartIcon,
      title: 'Build Empathy',
      description: 'Experience life through different perspectives and develop deeper understanding of others.',
    },
    {
      icon: GlobeAmericasIcon,
      title: 'Global Perspectives',
      description: 'Explore diverse cultures, backgrounds, and life situations from around the world.',
    },
    {
      icon: AcademicCapIcon,
      title: 'Interactive Learning',
      description: 'Engage with branching scenarios that adapt to your choices and decisions.',
    },
    {
      icon: TrophyIcon,
      title: 'Track Progress',
      description: 'Earn empathy points, unlock badges, and see your growth journey.',
    },
  ];

  const stats = [
    { label: 'Life Experiences', value: '50+' },
    { label: 'Countries Represented', value: '25+' },
    { label: 'Active Users', value: '1,000+' },
    { label: 'Empathy Points Earned', value: '100K+' },
  ];

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-br from-primary-50 to-empathy-50 overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                  <span className="block xl:inline">Experience Life</span>{' '}
                  <span className="block text-primary-600 xl:inline">Through Different Eyes</span>
                </h1>
                <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  Build empathy and understanding by walking in someone else's shoes. 
                  Explore real stories, make meaningful choices, and discover the power of perspective.
                </p>
                <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                  <div className="rounded-md shadow">
                    <Link
                      to={isAuthenticated ? "/experiences" : "/register"}
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 md:py-4 md:text-lg md:px-10"
                    >
                      {isAuthenticated ? "Explore Experiences" : "Get started"}
                    </Link>
                  </div>
                  <div className="mt-3 sm:mt-0 sm:ml-3">
                    <Link
                      to="/experiences"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200 md:py-4 md:text-lg md:px-10"
                    >
                      Browse Stories
                    </Link>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>
        <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
          <div className="h-56 w-full sm:h-72 md:h-96 lg:w-full lg:h-full bg-gradient-to-br from-primary-100 to-empathy-100 flex items-center justify-center">
            <div className="text-center">
              <HeartIcon className="h-24 w-24 text-primary-400 mx-auto mb-4" />
              <p className="text-lg text-gray-600">Empathy Through Experience</p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900">Making an Impact</h2>
            <p className="mt-4 text-lg text-gray-600">
              Join thousands of people building empathy across the globe
            </p>
          </div>
          <div className="mt-10">
            <dl className="grid grid-cols-2 gap-8 lg:grid-cols-4">
              {stats.map((stat) => (
                <div key={stat.label} className="text-center">
                  <dt className="text-3xl font-extrabold text-primary-600">{stat.value}</dt>
                  <dd className="mt-2 text-base text-gray-600">{stat.label}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900">
              How LifeSwap Works
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Experience, learn, and grow through immersive storytelling
            </p>
          </div>
          <div className="mt-16">
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
              {features.map((feature) => (
                <div key={feature.title} className="text-center">
                  <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mx-auto">
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <h3 className="mt-6 text-lg font-medium text-gray-900">{feature.title}</h3>
                  <p className="mt-2 text-base text-gray-500">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary-600">
        <div className="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
            <span className="block">Ready to expand your perspective?</span>
          </h2>
          <p className="mt-4 text-lg leading-6 text-primary-200">
            Join the LifeSwap community and start your journey of empathy and understanding today.
          </p>
          <Link
            to={isAuthenticated ? "/dashboard" : "/register"}
            className="mt-8 w-full inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-primary-50 sm:w-auto"
          >
            {isAuthenticated ? "Go to Dashboard" : "Sign up for free"}
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;