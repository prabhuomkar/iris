import React from 'react';
import Button from '@mui/material/Button';
import AddBoxIcon from '@mui/icons-material/AddBox';

const CreateAlbum = () => {
  return (
    <Button sx={{ color: 'gray', textTransform: 'none' }} variant="text">
      <AddBoxIcon sx={{ fontSize: '20px' }} /> &nbsp; Create album
    </Button>
  );
};

export default CreateAlbum;
