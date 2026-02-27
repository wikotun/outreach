import apiClient from './client';
import { Token, User, UserInput } from '../types';

export const authApi = {
  login: async (username: string, password: string): Promise<Token> => {
    const response = await apiClient.post<Token>(
      `/security/token?login=${encodeURIComponent(username)}&pwd=${encodeURIComponent(password)}`
    );
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
