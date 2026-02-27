import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, Users, Tags, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader } from '../components';
import { eventsApi, eventTypesApi, participantsApi } from '../api';
import { Event } from '../types';
import { format } from 'date-fns';

export function Dashboard() {
  const [stats, setStats] = useState({
    events: 0,
    eventTypes: 0,
    participants: 0,
  });
  const [upcomingEvents, setUpcomingEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [events, eventTypes, participants] = await Promise.all([
          eventsApi.list(),
          eventTypesApi.list(),
          participantsApi.list(),
        ]);

        setStats({
          events: events.length,
          eventTypes: eventTypes.length,
          participants: participants.length,
        });

        const sortedEvents = events
          .filter((e) => new Date(e.event_date) >= new Date())
          .sort((a, b) => new Date(a.event_date).getTime() - new Date(b.event_date).getTime())
          .slice(0, 5);

        setUpcomingEvents(sortedEvents);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="flex items-center gap-4 py-6">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Calendar className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.events}</p>
              <p className="text-sm text-gray-600">Total Events</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex items-center gap-4 py-6">
            <div className="p-3 bg-green-100 rounded-lg">
              <Tags className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.eventTypes}</p>
              <p className="text-sm text-gray-600">Event Types</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex items-center gap-4 py-6">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Users className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.participants}</p>
              <p className="text-sm text-gray-600">Participants</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Upcoming Events</h2>
            <Link
              to="/events"
              className="text-sm text-blue-600 hover:underline flex items-center gap-1"
            >
              View all <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </CardHeader>
        <CardContent>
          {upcomingEvents.length === 0 ? (
            <p className="text-gray-500 text-center py-4">No upcoming events</p>
          ) : (
            <div className="space-y-3">
              {upcomingEvents.map((event) => (
                <Link
                  key={event.id}
                  to={`/events/${event.id}`}
                  className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div>
                    <p className="font-medium text-gray-900">{event.name}</p>
                    <p className="text-sm text-gray-500">{event.location}</p>
                  </div>
                  <p className="text-sm text-gray-600">
                    {format(new Date(event.event_date), 'MMM d, yyyy')}
                  </p>
                </Link>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
