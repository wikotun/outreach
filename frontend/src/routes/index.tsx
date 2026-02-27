import { Routes, Route } from 'react-router-dom';
import { MainLayout, ProtectedRoute } from '../components';
import {
  Login,
  Register,
  Dashboard,
  EventsList,
  EventDetail,
  EventForm,
  EventTypesList,
  EventTypeForm,
  ParticipantsList,
  ParticipantForm,
  UsersList,
  Profile,
} from '../pages';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />

        <Route path="events">
          <Route index element={<EventsList />} />
          <Route path="new" element={<EventForm />} />
          <Route path=":id" element={<EventDetail />} />
          <Route path=":id/edit" element={<EventForm />} />
        </Route>

        <Route path="event-types">
          <Route index element={<EventTypesList />} />
          <Route path="new" element={<EventTypeForm />} />
          <Route path=":id/edit" element={<EventTypeForm />} />
        </Route>

        <Route path="participants">
          <Route index element={<ParticipantsList />} />
          <Route path="new" element={<ParticipantForm />} />
          <Route path=":id/edit" element={<ParticipantForm />} />
        </Route>

        <Route path="users">
          <Route index element={<UsersList />} />
        </Route>

        <Route path="profile" element={<Profile />} />
      </Route>
    </Routes>
  );
}
