import React, { useEffect, Suspense } from "react";
import { CircularProgress } from "@mui/material";

import { PositionsTable } from "../components";

export const Dashboard = () => {
  return (
    <Suspense fallback={<CircularProgress />}>
      <PositionsTable />
    </Suspense>
  );
};
