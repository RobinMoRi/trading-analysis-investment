import React, { Suspense, useEffect, useState } from "react";
import {
  Modal,
  Button,
  Box,
  FormControl,
  TextField,
  Typography,
  Stack,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";

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
  updatePositions,
  Position,
} from "../../api";

export const PositionsTable = () => {
  const [open, setOpen] = useState<boolean>(false);
  const [companies, setCompanies] = useState<Company[]>();
  const [netAssetValues, setNetAssetValues] = useState<AssetValue[]>();
  const [positions, setPositions] = useState<Position[]>();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const updateData = async () => {
    await updatePrices();
    await updateCompanies();
    await updateAssetValues();
  };

  console.log({ errors, errorPF: errors.portfolioSize });

  const handleUpdatePositions = () => {
    updatePositions(1000)
      .then((res) => console.log(res))
      .catch((err) => console.log(err));
  };

  const getData = async () => {
    const companies = await getCompanies();
    setCompanies(companies.data);

    const nav = await getAssetValues();
    setNetAssetValues(nav.data);

    const positions = await getPositions();
    setPositions(positions.data);
  };

  useEffect(() => {
    // getData();
  }, []);

  return (
    <Box sx={{ margin: (theme) => theme.spacing(2) }}>
      <Button variant="outlined" color="secondary" onClick={handleOpen}>
        Update Positions
      </Button>
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
            backgroundColor: "#ffffff40",
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
              <Button
                fullWidth
                variant="outlined"
                color="secondary"
                onClick={handleSubmit((data) => console.log(data))}
              >
                Submit
              </Button>
            </Stack>
          </FormControl>
        </Box>
      </Modal>
    </Box>
  );
};
