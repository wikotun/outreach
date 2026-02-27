export interface User {
  id: number;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface UserInput {
  username: string;
  password: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface EventType {
  id: number;
  name: string;
  description: string | null;
}

export interface EventTypeInput {
  name: string;
  description?: string | null;
}

export interface Event {
  id: number;
  name: string;
  event_date: string;
  description: string | null;
  location: string;
  event_type_id: number | null;
}

export interface EventInput {
  name: string;
  event_date: string;
  description?: string | null;
  location: string;
  event_type_id?: number | null;
}

export interface Participant {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  event_id: number | null;
}

export interface ParticipantInput {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  event_id?: number | null;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
