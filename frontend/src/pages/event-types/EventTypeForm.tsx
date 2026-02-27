import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ArrowLeft } from 'lucide-react';
import { eventTypesApi } from '../../api';
import { Button, Input, Card, CardHeader, CardContent } from '../../components';

const eventTypeSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().optional(),
});

type EventTypeFormData = z.infer<typeof eventTypeSchema>;

export function EventTypeForm() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditing = Boolean(id);
  const [isLoading, setIsLoading] = useState(isEditing);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<EventTypeFormData>({
    resolver: zodResolver(eventTypeSchema),
  });

  useEffect(() => {
    const fetchEventType = async () => {
      if (!id) return;
      try {
        const eventType = await eventTypesApi.get(Number(id));
        reset({
          name: eventType.name,
          description: eventType.description || '',
        });
      } catch (error) {
        console.error('Failed to fetch event type:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (isEditing) {
      fetchEventType();
    }
  }, [id, isEditing, reset]);

  const onSubmit = async (data: EventTypeFormData) => {
    setIsSaving(true);
    setError('');
    try {
      const eventTypeData = {
        name: data.name,
        description: data.description || null,
      };

      if (isEditing && id) {
        await eventTypesApi.update(Number(id), eventTypeData);
      } else {
        await eventTypesApi.create(eventTypeData);
      }
      navigate('/event-types');
    } catch {
      setError('Failed to save event type. Please try again.');
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
        <Link to="/event-types">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">
          {isEditing ? 'Edit Event Type' : 'New Event Type'}
        </h1>
      </div>

      <Card>
        <CardHeader>
          <h2 className="text-lg font-semibold">Event Type Details</h2>
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
              label="Name"
              error={errors.name?.message}
              {...register('name')}
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
              <Link to="/event-types">
                <Button variant="secondary" type="button">
                  Cancel
                </Button>
              </Link>
              <Button type="submit" disabled={isSaving}>
                {isSaving ? 'Saving...' : isEditing ? 'Update Event Type' : 'Create Event Type'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
