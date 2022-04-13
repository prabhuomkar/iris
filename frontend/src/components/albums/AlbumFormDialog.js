import React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import AlbumsStyled from './styles';

const AlbumFormDialog = ({ handleDialogClose, dialogOpen }) => {
  return (
    <div>
      <Dialog open={dialogOpen} onClose={handleDialogClose}>
        <DialogTitle>Rename album</DialogTitle>
        <DialogContent>
          <AlbumsStyled>
            <div className="album-dialog">
              <div>
                <img
                  src="https://images.unsplash.com/photo-1551963831-b3b1ca40c98e"
                  width="110px"
                  height="110px"
                  style={{ borderRadius: '6px' }}
                />
              </div>
              <div style={{ marginLeft: '16px' }}>
                <TextField
                  autoFocus
                  margin="dense"
                  id="name"
                  fullWidth
                  placeholder="Album name"
                  variant="standard"
                />
              </div>
            </div>
          </AlbumsStyled>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>Cancel</Button>
          <Button variant="contained" onClick={handleDialogClose}>
            Done
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default AlbumFormDialog;
