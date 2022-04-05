import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import SideNav from './components/sidenav/SideNav';
import Header from './components/header/Header';
import { Home, Explore, Sharing, PageNotFound } from './pages';

const App = () => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <Header handleDrawerToggle={handleDrawerToggle} />
      <Box
        component="nav"
        sx={{ width: { sm: 240 }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
      >
        <SideNav
          mobileOpen={mobileOpen}
          handleDrawerToggle={handleDrawerToggle}
        />
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - 240px)` },
        }}
      >
        <Toolbar />
        {/* content goes here */}
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/explore" element={<Explore />} />
          <Route exact path="/sharing" element={<Sharing />} />
          {/* library */}
          <Route exact path="/favourites" element={<>Favourites</>} />
          <Route exact path="/albums" element={<>Albums</>} />
          <Route exact path="/utilities" element={<>Utilities</>} />
          <Route exact path="/trash" element={<>Trash</>} />
          {/* page not found */}
          <Route path="*" element={<PageNotFound />} />
        </Routes>
      </Box>
    </Box>
  );
};

export default App;
