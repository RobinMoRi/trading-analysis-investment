import React, { useEffect } from "react";

import { updatePositions } from "../api";

export const Dashboard = () => {
  const init = async () => {
    const nav = await updatePositions(1000);
    console.log({ nav });
  };
  useEffect(() => {
    init();
  }, []);
  return <div>hejhej</div>;
};
