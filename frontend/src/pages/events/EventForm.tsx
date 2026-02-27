import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ArrowLeft } from 'lucide-react';
import { eventsApi, eventTypesApi } from '../../api';
import { EventType } from '../../types';
import { Button, Input, Select, Card, CardHeader, CardContent } from '../../components';

const eventSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  event_date: z.string().min(1, 'Date is required'),
  location: z.string().min(1, 'Location is required'),
  description: z.string().optional(),
  event_type_id: z.string().optional(),
});

type EventFormData = z.infer<typeof eventSchema>;

export function EventForm() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditing = Boolean(id);
  const [eventTypes, setEventTypes] = useState<EventType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<EventFormData>({
    resolver: zodResolver(eventSchema),
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const types = await eventTypesApi.list();
        setEventTypes(types);

        if (id) {
          const event = await eventsApi.get(Number(id));
          reset({
            name: event.name,
            event_date: event.event_date,
            location: event.location,
            description: event.description || '',
            event_type_id: event.event_type_id?.toString() || '',
          });
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [id, reset]);

  const onSubmit = async (data: EventFormData) => {
    setIsSaving(true);
    setError('');
    try {
      const eventData = {
        name: data.name,
        event_date: data.event_date,
        location: data.location,
        description: data.description || null,
        event_type_id: data.event_type_id ? Number(data.event_type_id) : null,
      };

      if (isEditing && id) {
        await eventsApi.update(Number(id), eventData);
      } else {
        await eventsApi.create(eventData);
      }
      navigate('/events');
    } catch {
      setError('Failed to save event. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
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
        <h1 className="text-2xl font-bold text-gray-900">
          {isEditing ? 'Edit Event' : 'New Event'}
        </h1>
      </div>

      <Card>
        <CardHeader>
          <h2 className="text-lg font-semibold">Event Details</h2>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <Input
              id="name"
              label="Event Name"
              error={errors.name?.message}
              {...register('name')}
            />

            <Input
              id="event_date"
              label="Date"
              type="date"
              error={errors.event_date?.message}
              {...register('event_date')}
            />

            <Input
              id="location"
              label="Location"
              error={errors.location?.message}
              {...register('location')}
            />

            <Select
              id="event_type_id"
              label="Event Type"
              error={errors.event_type_id?.message}
              options={[
                { value: '', label: 'Select a type (optional)' },
                ...eventTypes.map((type) => ({
                  value: type.id.toString(),
                  label: type.name,
                })),
              ]}
              {...register('event_type_id')}
            />

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                id="description"
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                {...register('description')}
              />
            </div>

            <div className="flex justify-end gap-3 pt-4">
              <Link to="/events">
                <Button variant="secondary" type="button">
                  Cancel
                </Button>
              </Link>
              <Button type="submit" disabled={isSaving}>
                {isSaving ? 'Saving...' : isEditing ? 'Update Event' : 'Create Event'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
