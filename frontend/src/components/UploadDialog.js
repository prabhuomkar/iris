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

const MUTATION = gql`
  mutation ($file: Upload!) {
    upload(file: $file)
  }
`;

const UploadDialog = ({ open, setOpen }) => {
  const [mutate, { data, loading, error }] = useMutation(MUTATION);
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
    // console.log(data.upload);
    setTimeout(() => {
      history.push('/');
      history.go(0);
      setOpen(false);
    }, 2000);
  }
  if (loading) {
    console.log(loading);
  }
  if (error) {
    console.log(error);
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
        <br />
        {loading && (
          <>
            <br />
            <LinearProgress />
          </>
        )}
        {data && data.upload && (
          <span style={{ color: 'green' }}>Photo uploaded successfully!</span>
        )}
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
