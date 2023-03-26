import React, { Suspense, useEffect, useState } from "react";
import {
  Modal,
  Button,
  Box,
  FormControl,
  TextField,
  Typography,
  Stack,
  Chip,
} from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import { DataGrid, GridColDef, GridValueGetterParams } from "@mui/x-data-grid";

import { useForm } from "react-hook-form";

import {
  getCompanies,
  updateCompanies,
  updatePrices,
  Company,
  getAssetValues,
  updateAssetValues,
  AssetValue,
  getPositions,
  ValueTypeEnum,
  AssetTypeEnum,
  updatePositions,
  Position,
  PositionDeep,
  getPositionsDeep,
} from "../../api";

type PortfolioSizeForm = {
  portfolioSize: number;
};

export const PositionsTable = () => {
  const [open, setOpen] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadingUpdate, setLoadingUpdate] = useState<boolean>(false);
  const [positions, setPositions] = useState<PositionDeep[]>([]);
  const [gridPositions, setGridPositions] = useState<any>([]);
  const [portfolioSize, setPortfolioSize] = useState<number>(0);
  const [totalValue, setTotalValue] = useState<{ type: string; val: number }[]>(
    []
  );
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PortfolioSizeForm>();

  useEffect(() => {
    getPositionsData();
  }, []);

  useEffect(() => {
    if (positions.length > 0) {
      handleGridRows();
    }
  }, [positions]);

  const handleGridRows = () => {
    const rows = [];
    let sumReported = 0;
    let sumComputed = 0;
    for (let position of positions) {
      let temp = {
        id: position.id,
        position: position.position,
        weight: position.weight,
        assetType: AssetTypeEnum[position.netassetvalue.asset_type],
        valueType: ValueTypeEnum[position.netassetvalue.value_type],
        company: position.company.name,
        price: position.company.price,
        buy: position.buy,
        val: position.val,
      };
      if (temp.valueType.toLowerCase() === "reported") {
        sumReported += position.val;
      } else {
        sumComputed += position.val;
      }
      rows.push(temp);
    }
    setGridPositions(rows);
    setTotalValue([
      { type: "reported", val: sumReported },
      { type: "computed", val: sumComputed },
    ]);
    setLoading(false);
  };

  const getPositionsData = async () => {
    const positions = await getPositionsDeep();
    setPositions(positions.data);
  };

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const updateData = async () => {
    await updatePrices();
    await updateCompanies();
    await updateAssetValues();
  };

  const handleUpdatePositions = (portfolioSize: number) => {
    setLoadingUpdate(true);
    setPortfolioSize(portfolioSize);
    updateData()
      .then(() => {
        return updatePositions(portfolioSize).then(() => {
          return getPositionsData();
        });
      })
      .then((res) => {
        console.log(res);
        setLoadingUpdate(false);
        handleClose();
      })
      .catch((err) => console.log(err));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <Box sx={{ margin: (theme) => theme.spacing(2) }}>
      <Stack spacing={2} sx={{ marginBottom: 2 }} direction="row">
        <Button variant="outlined" color="secondary" onClick={handleOpen}>
          Update Positions
        </Button>
        {totalValue.map((el) => (
          <Chip label={`Total buy sum (${el.type}): ${el.val}`} />
        ))}
        <Chip label={`Portfolio size: ${portfolioSize}`} />
      </Stack>
      <DataGrid
        autoHeight
        rows={gridPositions}
        columns={columns}
        pageSize={gridPositions.length}
        rowsPerPageOptions={[5]}
        checkboxSelection
      />

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Box
          sx={{
            backgroundColor: "#141B2D",
            padding: (theme) => theme.spacing(8),
            minWidth: (theme) => theme.spacing(30),
            borderRadius: "8px",
          }}
        >
          <FormControl
            sx={{
              height: "100%",
            }}
          >
            <Stack spacing={4}>
              <Typography>Update Positions</Typography>
              <TextField
                error={errors.portfolioSize !== undefined}
                label="Portfolio Size"
                fullWidth
                variant="outlined"
                color="secondary"
                {...register("portfolioSize", { pattern: /[0-9]+/ })}
              />
              <LoadingButton
                fullWidth
                loading={loadingUpdate}
                variant="outlined"
                color="secondary"
                onClick={handleSubmit((data) =>
                  handleUpdatePositions(data.portfolioSize)
                )}
              >
                Submit
              </LoadingButton>
            </Stack>
          </FormControl>
        </Box>
      </Modal>
    </Box>
  );
};

const columns: GridColDef[] = [
  { field: "id", headerName: "ID", width: 50 },
  {
    field: "company",
    headerName: "Company",
    width: 200,
  },
  {
    field: "assetType",
    headerName: "Asset Type",
    width: 150,
  },
  {
    field: "valueType",
    headerName: "Value Type",
    width: 150,
  },
  {
    field: "weight",
    headerName: "Weight",
    width: 150,
  },
  {
    field: "price",
    headerName: "Price",
    width: 150,
  },
  {
    field: "val",
    headerName: "Value (position based on buy sum)",
    width: 200,
  },

  {
    field: "buy",
    headerName: "Buy (no of stocks to buy)",
    width: 200,
  },
  {
    field: "position",
    headerName: "Position (based on weight)",
    width: 200,
  },
];
