import { useState } from 'react'
import { Routes, Route } from 'react-router-dom';
import { ColorModeContext, useMode } from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { ProSidebarProvider } from 'react-pro-sidebar';

import Topbar from './global/Topbar/Topbar';
import CustomSidebar from './global/CustomSidebar/CustomSidebar';

function App() {
  const [theme, colorMode] = useMode();

  return (
    <ProSidebarProvider>
      <ColorModeContext.Provider value={colorMode}>
          <ThemeProvider theme={theme}>
          <CssBaseline />
            <div className="app">
            <CustomSidebar />
            <main className="content">
            <Topbar />
            </main>
          </div>
          </ThemeProvider>
        </ColorModeContext.Provider>
    </ProSidebarProvider>
  )
}

export default App