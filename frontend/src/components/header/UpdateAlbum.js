import React from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';
import { gql, useMutation } from '@apollo/client';
import { TopAppBarActionItem } from '@rmwc/top-app-bar';
import { Snackbar } from '@rmwc/snackbar';
import { Button } from '@rmwc/button';
import { Error } from '..';

const UPDATE_ALBUM = gql`
  mutation updateAlbumMediaItems(
    $id: String!
    $type: String!
    $mediaItems: [String!]!
  ) {
    updateAlbumMediaItems(id: $id, type: $type, mediaItems: $mediaItems)
  }
`;

var pageURL = window.location.href;
var albumId = pageURL.split('/');

const UpdateAlbum = ({ disabled, removeImageList, addImageList }) => {
  const history = useHistory();
  const [updateAlbum, { data, error, loading }] = useMutation(UPDATE_ALBUM);
  const handleUpdate = (updatedList, type) => {
    type === 'add'
      ? updateAlbum({
          variables: {
            id: String(albumId[albumId.length - 2]),
            type: type,
            mediaItems: updatedList,
          },
        })
      : updateAlbum({
          variables: {
            id: String(albumId[albumId.length - 1]),
            type: type,
            mediaItems: updatedList,
          },
        });
  };

  if (loading)
    return (
      <Snackbar
        open={true}
        message={
          removeImageList
            ? 'Removing photos from album...'
            : 'Adding photos to album...'
        }
      />
    );

  if (data && data.updateAlbumMediaItems) {
    setTimeout(() => {
      if (removeImageList) {
        history.go(0);
      } else {
        history.push(`/album/${albumId[albumId.length - 2]}`);
      }
    });
    return (
      <Snackbar
        open={true}
        message={
          removeImageList
            ? 'Photo has been deleted'
            : 'Photo has been added to album'
        }
      />
    );
  }

  if (error) return <Error />;

  return (
    <>
      {removeImageList ? (
        <TopAppBarActionItem
          icon={disabled ? '' : 'remove_circle_outline'}
          style={{ color: 'red' }}
          disabled={disabled ? true : false}
          onClick={() => handleUpdate(removeImageList, 'remove')}
        />
      ) : (
        <Button
          icon="add"
          label={`Add (${addImageList.length})`}
          unelevated
          style={{ color: '#fff' }}
          disabled={disabled ? true : false}
          onClick={() => handleUpdate(addImageList, 'add')}
        />
      )}
    </>
  );
};

UpdateAlbum.propTypes = {
  disabled: PropTypes.bool,
  removeImageList: PropTypes.array,
  addImageList: PropTypes.array,
};

export default UpdateAlbum;
