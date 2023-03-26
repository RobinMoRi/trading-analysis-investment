import React from "react";
import { Box, Stack } from "@mui/material";
import { TwitterTimelineEmbed } from "react-twitter-embed";

export const Twitter = () => {
  return (
    <Box sx={{ p: 2 }}>
      <Stack direction="row">
        <TwitterTimelineEmbed
          sourceType="profile"
          screenName="ibindex"
          options={{ height: 600, width: 400 }}
        />
        <TwitterTimelineEmbed
          sourceType="profile"
          screenName="avanzabank"
          options={{ height: 600, width: 400 }}
        />
      </Stack>
    </Box>
  );
};
