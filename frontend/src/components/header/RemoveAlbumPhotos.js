import React from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';
import { gql, useMutation } from '@apollo/client';
import { TopAppBarActionItem } from '@rmwc/top-app-bar';
import { Snackbar } from '@rmwc/snackbar';
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
var albumId = pageURL.substr(pageURL.lastIndexOf('/') + 1);

const RemoveAlbumPhotos = ({ disabled, removeImageList }) => {
  const history = useHistory();
  const [updateAlbum, { data, error, loading }] = useMutation(UPDATE_ALBUM);
  const handleRemove = (removeImageList) => {
    updateAlbum({
      variables: { id: albumId, type: 'remove', mediaItems: removeImageList },
    });
  };

  if (loading)
    return <Snackbar open={true} message={'Removing photos from album...'} />;

  if (data && data.updateAlbumMediaItems) {
    setTimeout(() => {
      history.go(0);
    });
    return <Snackbar open={true} message={'Photo has been deleted'} />;
  }

  if (error) return <Error />;

  return (
    <>
      <TopAppBarActionItem
        icon={disabled ? '' : 'remove_circle_outline'}
        style={{ color: 'red' }}
        disabled={disabled ? true : false}
        onClick={() => handleRemove(removeImageList)}
      />
    </>
  );
};

RemoveAlbumPhotos.propTypes = {
  disabled: PropTypes.bool,
  removeImageList: PropTypes.array,
};

export default RemoveAlbumPhotos;
