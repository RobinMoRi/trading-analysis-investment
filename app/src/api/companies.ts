import { client } from ".";

export type Company = {
  ticker: string;
  yf_ticker: string;
  name: string;
  price: number;
  id: number;
};

export type Price = {
  yf_ticker: string;
  price: number;
  price_updated_at: string;
};

export const getCompanies = (skip = 0, limit = 100) => {
  return client.get<Company[]>(`/companies/?skip=${skip}&limit=${limit}`);
};

export const updateCompanies = () => {
  return client.post<Company[]>("/companies/update");
};

export const getPrices = (skip = 0, limit = 100) => {
  return client.get<Price[]>(`/companies/prices/?skip=${skip}&limit=${limit}`);
};

export const updatePrices = () => {
  return client.post<Price[]>("/companies/prices");
};
