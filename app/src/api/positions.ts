import { client } from ".";

export type Position = {
  yf_ticker: string;
  reported_weight: number;
  computed_weight: number;
  reported_position: number;
  computed_position: number;
  reported_buy: number;
  computed_buy: number;
};

export const getPositions = (skip = 0, limit = 100) => {
  return client.get<Position[]>(
    `/companies/positions/?skip=${skip}&limit=${limit}`
  );
};

export const updatePositions = (portfolioSize: number = 0) => {
  return client.post<Position[]>(
    `/companies/positions/?portfolio_size=${portfolioSize}`
  );
};
