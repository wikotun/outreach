import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { ArrowLeft } from 'lucide-react';
import { participantsApi, eventsApi } from '../../api';
import { Event } from '../../types';
import { Button, Input, Select, Card, CardHeader, CardContent } from '../../components';

const participantSchema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name: z.string().min(1, 'Last name is required'),
  email: z.string().email('Invalid email address'),
  phone: z.string().min(1, 'Phone is required'),
  address: z.string().min(1, 'Address is required'),
  city: z.string().min(1, 'City is required'),
  state: z.string().min(2, 'State is required').max(2, 'Use 2-letter state code'),
  zip_code: z.string().min(5, 'ZIP code is required'),
  event_id: z.string().optional(),
});

type ParticipantFormData = z.infer<typeof participantSchema>;

export function ParticipantForm() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditing = Boolean(id);
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ParticipantFormData>({
    resolver: zodResolver(participantSchema),
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const eventsData = await eventsApi.list();
        setEvents(eventsData);

        if (id) {
          const participant = await participantsApi.get(Number(id));
          reset({
            first_name: participant.first_name,
            last_name: participant.last_name,
            email: participant.email,
            phone: participant.phone,
            address: participant.address,
            city: participant.city,
            state: participant.state,
            zip_code: participant.zip_code,
            event_id: participant.event_id?.toString() || '',
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

  const onSubmit = async (data: ParticipantFormData) => {
    setIsSaving(true);
    setError('');
    try {
      const participantData = {
        first_name: data.first_name,
        last_name: data.last_name,
        email: data.email,
        phone: data.phone,
        address: data.address,
        city: data.city,
        state: data.state,
        zip_code: data.zip_code,
        event_id: data.event_id ? Number(data.event_id) : null,
      };

      if (isEditing && id) {
        await participantsApi.update(Number(id), participantData);
      } else {
        await participantsApi.create(participantData);
      }
      navigate('/participants');
    } catch {
      setError('Failed to save participant. Please try again.');
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
        <Link to="/participants">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">
          {isEditing ? 'Edit Participant' : 'New Participant'}
        </h1>
      </div>

      <Card>
        <CardHeader>
          <h2 className="text-lg font-semibold">Participant Details</h2>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                id="first_name"
                label="First Name"
                error={errors.first_name?.message}
                {...register('first_name')}
              />
              <Input
                id="last_name"
                label="Last Name"
                error={errors.last_name?.message}
                {...register('last_name')}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                id="email"
                label="Email"
                type="email"
                error={errors.email?.message}
                {...register('email')}
              />
              <Input
                id="phone"
                label="Phone"
                error={errors.phone?.message}
                {...register('phone')}
              />
            </div>

            <Input
              id="address"
              label="Address"
              error={errors.address?.message}
              {...register('address')}
            />

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="col-span-2">
                <Input
                  id="city"
                  label="City"
                  error={errors.city?.message}
                  {...register('city')}
                />
              </div>
              <Input
                id="state"
                label="State"
                placeholder="CA"
                error={errors.state?.message}
                {...register('state')}
              />
              <Input
                id="zip_code"
                label="ZIP Code"
                error={errors.zip_code?.message}
                {...register('zip_code')}
              />
            </div>

            <Select
              id="event_id"
              label="Event"
              error={errors.event_id?.message}
              options={[
                { value: '', label: 'Select an event (optional)' },
                ...events.map((event) => ({
                  value: event.id.toString(),
                  label: event.name,
                })),
              ]}
              {...register('event_id')}
            />

            <div className="flex justify-end gap-3 pt-4">
              <Link to="/participants">
                <Button variant="secondary" type="button">
                  Cancel
                </Button>
              </Link>
              <Button type="submit" disabled={isSaving}>
                {isSaving ? 'Saving...' : isEditing ? 'Update Participant' : 'Create Participant'}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
