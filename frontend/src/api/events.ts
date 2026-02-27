import apiClient from './client';
import { Event, EventInput } from '../types';

export const eventsApi = {
  list: async (): Promise<Event[]> => {
    const response = await apiClient.get<Event[]>('/event/list');
    return response.data;
  },

  get: async (id: number): Promise<Event> => {
    const response = await apiClient.get<Event>(`/event/read/${id}`);
    return response.data;
  },

  create: async (event: EventInput): Promise<Event> => {
    const response = await apiClient.post<Event>('/event/create', event);
    return response.data;
  },

  update: async (id: number, event: EventInput): Promise<Event> => {
    const response = await apiClient.put<Event>(`/event/update/${id}`, event);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/event/delete/${id}`);
  },

  listByDateRange: async (startDate: string, endDate: string): Promise<Event[]> => {
    const response = await apiClient.get<Event[]>(`/event/list/${startDate}/${endDate}`);
    return response.data;
  },
};
