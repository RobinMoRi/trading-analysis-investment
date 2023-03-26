import { client } from ".";

export type ValueType = "reported" | "computed" | "";
export type AssetType = "rebate" | "premium" | "";
export enum ValueTypeEnum {
  REPORTED,
  COMPUTED,
}

export enum AssetTypeEnum {
  REBATE,
  PREMIUM,
}

export type AssetValue = {
  ticker: string;
  val: number;
  value_type: number;
  asset_type: number;
  id: number;
};

export const getAssetValues = (
  skip = 0,
  limit = 100,
  valueType: ValueType = "",
  assetType: AssetType = ""
) => {
  const params = new URLSearchParams();
  if (valueType !== "") {
    params.append("value_type", valueType);
  }
  if (assetType !== "") {
    params.append("asset_type", assetType);
  }
  return client.get<AssetValue[]>(
    `/companies/asset-values/?skip=${skip}&limit=${limit}`,
    {
      params: params,
    }
  );
};

export const updateAssetValues = () => {
  return client.post<AssetValue[]>("/companies/asset-values");
};
