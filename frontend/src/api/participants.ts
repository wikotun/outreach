import apiClient from './client';
import { Participant, ParticipantInput } from '../types';

export const participantsApi = {
  list: async (): Promise<Participant[]> => {
    const response = await apiClient.get<Participant[]>('/participant/list');
    return response.data;
  },

  get: async (id: number): Promise<Participant> => {
    const response = await apiClient.get<Participant>(`/participant/read/${id}`);
    return response.data;
  },

  create: async (participant: ParticipantInput): Promise<Participant> => {
    const response = await apiClient.post<Participant>('/participant/create', participant);
    return response.data;
  },

  update: async (id: number, participant: ParticipantInput): Promise<Participant> => {
    const response = await apiClient.put<Participant>(`/participant/update/${id}`, participant);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/participant/delete/${id}`);
  },

  addToEvent: async (eventId: number, participant: ParticipantInput): Promise<Event> => {
    const response = await apiClient.post<Event>(`/event/participant/add/${eventId}`, participant);
    return response.data;
  },
};
