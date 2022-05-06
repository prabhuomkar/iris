import React from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';
import { gql, useMutation } from '@apollo/client';
import { CircularProgress } from '@rmwc/circular-progress';
import { Snackbar } from '@rmwc/snackbar';
import { Dialog, DialogTitle, DialogActions, DialogButton } from '@rmwc/dialog';
import '@rmwc/dialog/styles';

const DELETE_ALBUM = gql`
  mutation deleteAlbum($id: String!) {
    deleteAlbum(id: $id)
  }
`;

const DeleteAlbum = ({ openDelete, setOpenDelete, albumId, albumName }) => {
  const history = useHistory();
  const [deleteAlbum, { data: delData, loading: delLoading, error: delError }] =
    useMutation(DELETE_ALBUM);

  const handleDeleteAlbum = (albumId) => {
    deleteAlbum({
      variables: { id: albumId },
    });
  };

  if (delData && delData.deleteAlbum) {
    setTimeout(() => {
      history.push('/albums');
    }, 2000);
    return <Snackbar open={true} message={'Album has been deleted'} />;
  }

  return (
    <Dialog
      open={openDelete}
      onClose={() => {
        setOpenDelete(false);
      }}
    >
      <DialogTitle>
        Are you sure you want to delete album &quot;{albumName}&quot;?
      </DialogTitle>
      <br />
      <br />
      <DialogActions>
        {delLoading && <CircularProgress size="small" />} &nbsp;&nbsp;
        {delError && <>Sorry, some error occured!</>} &nbsp;&nbsp;
        <DialogButton
          unelevated
          onClick={() => handleDeleteAlbum(albumId)}
          style={{ color: '#fff' }}
        >
          Delete
        </DialogButton>
        &nbsp;&nbsp;
        <DialogButton outlined action="close">
          Close
        </DialogButton>
      </DialogActions>
    </Dialog>
  );
};

DeleteAlbum.propTypes = {
  openDelete: PropTypes.bool,
  setOpenDelete: PropTypes.func,
  albumId: PropTypes.string,
  albumName: PropTypes.string,
};

export default DeleteAlbum;
