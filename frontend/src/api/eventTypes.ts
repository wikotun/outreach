import apiClient from './client';
import { EventType, EventTypeInput } from '../types';

export const eventTypesApi = {
  list: async (): Promise<EventType[]> => {
    const response = await apiClient.get<EventType[]>('/type/list');
    return response.data;
  },

  get: async (id: number): Promise<EventType> => {
    const response = await apiClient.get<EventType>(`/type/read/${id}`);
    return response.data;
  },

  create: async (eventType: EventTypeInput): Promise<EventType> => {
    const response = await apiClient.post<EventType>('/type/create', eventType);
    return response.data;
  },

  update: async (id: number, eventType: EventTypeInput): Promise<EventType> => {
    const response = await apiClient.put<EventType>(`/type/update/${id}`, eventType);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/type/delete/${id}`);
  },
};
