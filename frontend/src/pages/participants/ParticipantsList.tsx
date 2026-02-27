import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Pencil, Trash2 } from 'lucide-react';
import { participantsApi, eventsApi } from '../../api';
import { Participant, Event } from '../../types';
import {
  Button,
  Card,
  CardHeader,
  CardContent,
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
  Modal,
} from '../../components';

export function ParticipantsList() {
  const [participants, setParticipants] = useState<Participant[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [participantsData, eventsData] = await Promise.all([
        participantsApi.list(),
        eventsApi.list(),
      ]);
      setParticipants(participantsData);
      setEvents(eventsData);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteId) return;
    try {
      await participantsApi.delete(deleteId);
      setParticipants(participants.filter((p) => p.id !== deleteId));
      setDeleteId(null);
    } catch (error) {
      console.error('Failed to delete participant:', error);
    }
  };

  const getEventName = (eventId: number | null) => {
    if (!eventId) return '-';
    const event = events.find((e) => e.id === eventId);
    return event?.name || '-';
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
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Participants</h1>
        <Link to="/participants/new">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            New Participant
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <h2 className="text-lg font-semibold">All Participants</h2>
        </CardHeader>
        <CardContent className="p-0">
          {participants.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No participants found</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Phone</TableHead>
                  <TableHead>City</TableHead>
                  <TableHead>Event</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {participants.map((participant) => (
                  <TableRow key={participant.id}>
                    <TableCell className="font-medium">
                      {participant.first_name} {participant.last_name}
                    </TableCell>
                    <TableCell>{participant.email}</TableCell>
                    <TableCell>{participant.phone}</TableCell>
                    <TableCell>{participant.city}, {participant.state}</TableCell>
                    <TableCell>{getEventName(participant.event_id)}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex items-center justify-end gap-2">
                        <Link to={`/participants/${participant.id}/edit`}>
                          <Button variant="ghost" size="sm">
                            <Pencil className="h-4 w-4" />
                          </Button>
                        </Link>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setDeleteId(participant.id)}
                        >
                          <Trash2 className="h-4 w-4 text-red-500" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      <Modal
        isOpen={deleteId !== null}
        onClose={() => setDeleteId(null)}
        title="Delete Participant"
      >
        <p className="text-gray-600 mb-4">
          Are you sure you want to delete this participant? This action cannot be undone.
        </p>
        <div className="flex justify-end gap-3">
          <Button variant="secondary" onClick={() => setDeleteId(null)}>
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
