import { useAuth } from '../../contexts/AuthContext';
import { Card, CardHeader, CardContent } from '../../components';
import { User, Mail, AtSign } from 'lucide-react';

export function Profile() {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>

      <Card>
        <CardHeader>
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
              <User className="h-8 w-8 text-blue-600" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {user.first_name} {user.last_name}
              </h2>
              <p className="text-gray-500">@{user.username}</p>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <AtSign className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Username</p>
                <p className="text-gray-900">{user.username}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Mail className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Email</p>
                <p className="text-gray-900">{user.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <User className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Full Name</p>
                <p className="text-gray-900">{user.first_name} {user.last_name}</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
