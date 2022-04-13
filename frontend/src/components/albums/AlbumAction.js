import React, { useState } from 'react';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import AlbumFormDialog from './AlbumFormDialog';

const AlbumAction = () => {
  const [anchor, setAnchor] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const open = Boolean(anchor);

  const handleClick = (event) => {
    setAnchor(event.currentTarget);
  };

  const handleClose = () => {
    setAnchor(null);
  };

  const handleDialogClickOpen = () => {
    setDialogOpen(true);
    setAnchor(null);
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
  };

  return (
    <div>
      <MoreVertIcon onClick={handleClick} sx={{ fontSize: '28px' }} />
      <Menu id="basic-menu" anchorEl={anchor} open={open} onClose={handleClose}>
        <MenuItem onClick={handleDialogClickOpen}>Rename album</MenuItem>
        <MenuItem onClick={handleClose}>Delete album</MenuItem>
      </Menu>
      <AlbumFormDialog
        handleDialogClickOpen={handleDialogClickOpen}
        handleDialogClose={handleDialogClose}
        dialogOpen={dialogOpen}
        setDialogOpen={setDialogOpen}
      />
    </div>
  );
};

export default AlbumAction;
