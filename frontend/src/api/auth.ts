import apiClient from './client';
import { Token, User, UserInput } from '../types';

export const authApi = {
  login: async (username: string, password: string): Promise<Token> => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    const response = await apiClient.post<Token>('/security/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  register: async (user: UserInput): Promise<User> => {
    const response = await apiClient.post<User>('/user/create', user);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/security/users/me');
    return response.data;
  },
};
