import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.username}!
        </h1>
        <p className="text-gray-600 mt-2">
          Continue your empathy journey and explore new perspectives.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Empathy Points</h3>
          <p className="text-3xl font-bold text-empathy-600">{user?.empathy_points || 0}</p>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Experiences</h3>
          <p className="text-3xl font-bold text-primary-600">{user?.total_experiences || 0}</p>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Level</h3>
          <p className="text-3xl font-bold text-green-600">
            {Math.floor((user?.total_experiences || 0) / 2) + 1}
          </p>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <p className="text-gray-600">No recent activity yet. Start exploring experiences!</p>
      </div>
    </div>
  );
};

export default Dashboard;