import React from 'react';
import PropTypes from 'prop-types';
import { gql, useMutation } from '@apollo/client';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogButton,
} from '@rmwc/dialog';
import '@rmwc/dialog/styles';

const MUTATION = gql`
  mutation ($file: Upload!) {
    upload(file: $file)
  }
`;

const UploadDialog = ({ open, setOpen }) => {
  const [mutate, { data, loading }] = useMutation(MUTATION);

  function onChange({
    target: {
      validity,
      files: [file],
    },
  }) {
    if (validity.valid) mutate({ variables: { file } });
  }

  console.log(data);
  console.log(loading);
  if (loading) {
    console.log('Uploading...');
    setOpen(false);
  }
  if (data && data.upload) {
    console.log('Photo Uploaded!');
  }

  return (
    <Dialog
      open={open}
      onClose={(evt) => {
        console.log(evt.detail.action);
        setOpen(false);
      }}
      onClosed={(evt) => console.log(evt.detail.action)}
    >
      <DialogTitle>Upload Photo</DialogTitle>
      <DialogContent>
        <input type="file" required onChange={onChange} />
      </DialogContent>
      <DialogActions>
        <DialogButton action="close">Close</DialogButton>
      </DialogActions>
    </Dialog>
  );
};

UploadDialog.propTypes = {
  open: PropTypes.bool,
  setOpen: PropTypes.func,
};

export default UploadDialog;
