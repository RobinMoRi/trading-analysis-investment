import { client } from ".";
import { Company, AssetValue } from ".";

export type Position = {
  id: number;
  val: number;
  weight: number;
  position: number;
  buy: number;
  value_type: number;
  company_id: number;
  netassetvalue_id: number;
};

export type PositionDeep = Position & {
  netassetvalue: AssetValue;
  company: Company;
};

export const getPositions = (skip = 0, limit = 100) => {
  return client.get<Position[]>(
    `/companies/positions/?skip=${skip}&limit=${limit}`
  );
};

export const getPositionsDeep = (skip = 0, limit = 100) => {
  return client.get<PositionDeep[]>(
    `/companies/positions/deep/?skip=${skip}&limit=${limit}`
  );
};

export const updatePositions = (portfolioSize: number) => {
  return client.post<Position[]>(
    `/companies/positions/?portfolio_size=${portfolioSize}`
  );
};
