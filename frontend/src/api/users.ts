import apiClient from './client';
import { User, UserInput } from '../types';

export const usersApi = {
  list: async (): Promise<User[]> => {
    const response = await apiClient.get<User[]>('/user/list');
    return response.data;
  },

  get: async (id: number): Promise<User> => {
    const response = await apiClient.get<User>(`/user/read/${id}`);
    return response.data;
  },

  findByUsername: async (username: string): Promise<User> => {
    const response = await apiClient.get<User>(`/user/find/${username}`);
    return response.data;
  },

  create: async (user: UserInput): Promise<User> => {
    const response = await apiClient.post<User>('/user/create', user);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/user/delete/${id}`);
  },
};
