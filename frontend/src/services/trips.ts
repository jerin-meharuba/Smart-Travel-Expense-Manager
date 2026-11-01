import type { Trip, TripFormValues, TripListResponse } from "../types/trip";
import api from "./api";

function toPayload(values: TripFormValues) {
  return {
    name: values.name,
    destination: values.destination,
    start_date: values.start_date,
    end_date: values.end_date,
    status: values.status,
  };
}

export const tripApi = {
  async list(): Promise<TripListResponse> {
    const response = await api.get<TripListResponse>("/trips", {
      params: { offset: 0, limit: 100 },
    });
    return response.data;
  },

  async create(values: TripFormValues): Promise<Trip> {
    const response = await api.post<Trip>("/trips", toPayload(values));
    return response.data;
  },

  async update(id: number, values: TripFormValues): Promise<Trip> {
    const response = await api.patch<Trip>(`/trips/${id}`, toPayload(values));
    return response.data;
  },

  async remove(id: number): Promise<void> {
    await api.delete(`/trips/${id}`);
  },
};
