import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Pencil, Trash2, MapPin, Calendar, Tag } from 'lucide-react';
import { format } from 'date-fns';
import { eventsApi, eventTypesApi } from '../../api';
import { Event, EventType } from '../../types';
import { Button, Card, CardHeader, CardContent, Modal } from '../../components';

export function EventDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [event, setEvent] = useState<Event | null>(null);
  const [eventType, setEventType] = useState<EventType | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    const fetchEvent = async () => {
      if (!id) return;
      try {
        const eventData = await eventsApi.get(Number(id));
        setEvent(eventData);

        if (eventData.event_type_id) {
          const typeData = await eventTypesApi.get(eventData.event_type_id);
          setEventType(typeData);
        }
      } catch (error) {
        console.error('Failed to fetch event:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchEvent();
  }, [id]);

  const handleDelete = async () => {
    if (!id) return;
    try {
      await eventsApi.delete(Number(id));
      navigate('/events');
    } catch (error) {
      console.error('Failed to delete event:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Event not found</p>
        <Link to="/events" className="text-blue-600 hover:underline mt-2 inline-block">
          Back to Events
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to="/events">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{event.name}</h1>
              {eventType && (
                <span className="inline-flex items-center gap-1 mt-2 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  <Tag className="h-3 w-3" />
                  {eventType.name}
                </span>
              )}
            </div>
            <div className="flex gap-2">
              <Link to={`/events/${id}/edit`}>
                <Button variant="secondary" size="sm">
                  <Pencil className="h-4 w-4 mr-2" />
                  Edit
                </Button>
              </Link>
              <Button
                variant="danger"
                size="sm"
                onClick={() => setShowDeleteModal(true)}
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div className="flex items-center gap-3 text-gray-600">
              <Calendar className="h-5 w-5" />
              <span>{format(new Date(event.event_date), 'EEEE, MMMM d, yyyy')}</span>
            </div>

            <div className="flex items-center gap-3 text-gray-600">
              <MapPin className="h-5 w-5" />
              <span>{event.location}</span>
            </div>

            {event.description && (
              <div className="mt-4">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Description</h3>
                <p className="text-gray-900">{event.description}</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete Event"
      >
        <p className="text-gray-600 mb-4">
          Are you sure you want to delete "{event.name}"? This action cannot be undone.
        </p>
        <div className="flex justify-end gap-3">
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            Delete
          </Button>
        </div>
      </Modal>
    </div>
  );
}
