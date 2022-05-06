import React from 'react';
import PropTypes from 'prop-types';
import { TextField } from '@rmwc/textfield';
import { Dialog, DialogTitle, DialogActions, DialogButton } from '@rmwc/dialog';

const RenameAlbum = ({ openRename, setOpenRename }) => {
  return (
    <>
      <Dialog
        open={openRename}
        onClose={() => {
          setOpenRename(false);
        }}
      >
        <DialogTitle>Rename album</DialogTitle>
        <br />
        <TextField
          //defaultValue={updatedAlbumName}
          //onChange={(e) => setupdatedAlbumName(e.target.value)}
          style={{ margin: '0px 20px' }}
        />
        <br />
        <DialogActions>
          <DialogButton unelevated style={{ color: '#fff' }}>
            Done
          </DialogButton>
          &nbsp;&nbsp;
          <DialogButton outlined action="close">
            Close
          </DialogButton>
        </DialogActions>
      </Dialog>
    </>
  );
};

RenameAlbum.propTypes = {
  openRename: PropTypes.bool,
  setOpenRename: PropTypes.func,
};

export default RenameAlbum;
