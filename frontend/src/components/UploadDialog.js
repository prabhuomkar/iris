import React from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';
import { gql, useMutation } from '@apollo/client';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogButton,
} from '@rmwc/dialog';
import '@rmwc/dialog/styles';
import { LinearProgress } from '@rmwc/linear-progress';
import '@rmwc/linear-progress/styles';

const UPLOAD_IMAGE = gql`
  mutation ($file: Upload!) {
    upload(file: $file)
  }
`;

const UploadDialog = ({ open, setOpen }) => {
  const [mutate, { data, loading, error }] = useMutation(UPLOAD_IMAGE);
  let history = useHistory();

  const onChange = ({
    target: {
      validity,
      files: [file],
    },
  }) => {
    if (validity.valid) mutate({ variables: { file } });
  };

  if (data && data.upload) {
    history.push('/');
    history.go(0);
    setOpen(false);
  }

  return (
    <Dialog
      open={open}
      onClose={() => {
        setOpen(false);
      }}
    >
      <DialogTitle>Upload Photo</DialogTitle>
      <DialogContent>
        <input
          type="file"
          accept="image/jpeg, image/png, image/bmp"
          required
          onChange={onChange}
        />
        <br />
        <br />
        <span style={{ fontSize: '15px', color: '#FF5722' }}>
          Currently only supports, .png, .jpg and .bmp format
        </span>
        <br />
        {loading && (
          <>
            <br />
            <LinearProgress />
          </>
        )}
        {error && (
          <>
            <br /> <span>Sorry, some error occured.</span>
          </>
        )}
        {data && data.upload && (
          <>
            <br />
            <span style={{ color: '#33691E' }}>Done!</span>
          </>
        )}
      </DialogContent>
      <DialogActions>
        <DialogButton outlined action="close">
          Close
        </DialogButton>
      </DialogActions>
    </Dialog>
  );
};

UploadDialog.propTypes = {
  open: PropTypes.bool,
  setOpen: PropTypes.func,
};

export default UploadDialog;
