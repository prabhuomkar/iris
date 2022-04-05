import React from 'react';
import { useNavigate } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Typography from '@mui/material/Typography';
import Toolbar from '@mui/material/Toolbar';

const Header = ({ handleDrawerToggle }) => {
  const navigate = useNavigate();

  const refresh = () => {
    window.location.reload();
  };

  return (
    <AppBar
      position="fixed"
      style={{ background: '#812ce5' }}
      sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={handleDrawerToggle}
          sx={{ mr: 2, display: { sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap component="div">
          <div
            style={{ display: 'flex', cursor: 'pointer' }}
            onClick={() => {
              navigate('/');
              refresh();
            }}
          >
            <img src="/logo.png" width="32px" />
            &nbsp; <div>iris</div>
          </div>
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
