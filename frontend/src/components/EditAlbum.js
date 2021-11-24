import React, { useState } from 'react';
import { gql, useMutation } from '@apollo/client';
import PropTypes from 'prop-types';
import { Icon } from '@rmwc/icon';
import { Button } from '@rmwc/button';
import { TextField } from '@rmwc/textfield';
import { CircularProgress } from '@rmwc/circular-progress';

const UPDATE_ALBUM = gql`
  mutation updateAlbum($id: String!, $name: String!) {
    updateAlbum(id: $id, input: { name: $name })
  }
`;

const EditAlbum = ({ albumId, albumName }) => {
  const [
    updateAlbum,
    { loading: updateAlbumNameLoading, error: updateAlbumNameyError },
  ] = useMutation(UPDATE_ALBUM);

  const [showEdit, setShowEdit] = useState(false);
  const [updatedAlbumName, setupdatedAlbumName] = useState(albumName);

  const handleEditAlbumName = (albumId, updatedAlbumName) => {
    updateAlbum({ variables: { id: albumId, name: updatedAlbumName } });
    setShowEdit(false);
  };

  return (
    <>
      {showEdit ? (
        <>
          <div className="edit-section">
            <TextField
              defaultValue={updatedAlbumName}
              onChange={(e) => setupdatedAlbumName(e.target.value)}
              style={{ height: '36px' }}
            />
            &nbsp;&nbsp;&nbsp;
            <Button
              onClick={() => handleEditAlbumName(albumId, updatedAlbumName)}
              label="update"
              unelevated
              disabled={updatedAlbumName ? false : true}
              style={{ color: '#fff' }}
            />
            &nbsp;&nbsp;&nbsp;
            <Button
              onClick={() => setShowEdit(!showEdit)}
              label="cancel"
              outlined
            />
            &nbsp;&nbsp;&nbsp;
            {updateAlbumNameLoading && <CircularProgress size="medium" />}
            {updateAlbumNameyError && (
              <>Sorry, some error occured while updating name</>
            )}
          </div>
          <br />
          <br />
        </>
      ) : (
        <>
          <h2>{updatedAlbumName}</h2>
          &nbsp;&nbsp;&nbsp;
          <Icon
            onClick={() => setShowEdit(!showEdit)}
            style={{ cursor: 'pointer', color: '#424242' }}
            icon={{ icon: 'edit', size: 'small' }}
          />
        </>
      )}
    </>
  );
};

EditAlbum.propTypes = {
  albumId: PropTypes.string,
  albumName: PropTypes.string,
};

export default EditAlbum;
