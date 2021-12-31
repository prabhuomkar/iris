import React from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';
import { gql, useMutation } from '@apollo/client';
import { TopAppBarActionItem } from '@rmwc/top-app-bar';
import { Snackbar } from '@rmwc/snackbar';
import { Button } from '@rmwc/button';
import { Error } from '.';

const UPDATE_ALBUM = gql`
  mutation updateAlbumMediaItems(
    $id: String!
    $type: String!
    $mediaItems: [String!]!
  ) {
    updateAlbumMediaItems(id: $id, type: $type, mediaItems: $mediaItems)
  }
`;

const UpdateAlbum = ({ disabled, albumId, removeImageList, addImageList }) => {
  const history = useHistory();
  const [updateAlbum, { data, error, loading }] = useMutation(UPDATE_ALBUM);

  const handleUpdateAlbum = (updatedList, type) => {
    updateAlbum({
      variables: {
        id: albumId,
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
        history.push(`/album/${albumId}`);
      }
    });
    return (
      <Snackbar
        open={true}
        message={
          removeImageList
            ? 'Photo has been removed'
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
          onClick={() => handleUpdateAlbum(removeImageList, 'remove')}
        />
      ) : (
        <Button
          icon="add"
          label={`Add (${addImageList.length})`}
          unelevated
          style={{ color: '#fff' }}
          disabled={disabled ? true : false}
          onClick={() => handleUpdateAlbum(addImageList, 'add')}
        />
      )}
    </>
  );
};

UpdateAlbum.propTypes = {
  disabled: PropTypes.bool,
  removeImageList: PropTypes.array,
  addImageList: PropTypes.array,
  albumId: PropTypes.string,
};

export default UpdateAlbum;
