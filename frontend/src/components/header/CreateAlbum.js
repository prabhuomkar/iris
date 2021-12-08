import React from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';
import { gql, useMutation } from '@apollo/client';
import { TopAppBarActionItem } from '@rmwc/top-app-bar';
import { Snackbar } from '@rmwc/snackbar';
import { Error } from '..';

const CREATE_ALBUM = gql`
  mutation createAlbum($mediaItems: [String]) {
    createAlbum(input: { name: "New Album", mediaItems: $mediaItems })
  }
`;

const CreateAlbum = ({ disabled, imageList }) => {
  const history = useHistory();
  const [updateAlbum, { data, error, loading }] = useMutation(CREATE_ALBUM);

  const handleUpdateAlbum = (imageList) => {
    updateAlbum({
      variables: { mediaItems: imageList },
    });
  };

  if (loading)
    return <Snackbar open={true} message={'Creating new album...'} />;

  if (data && data.createAlbum) {
    setTimeout(() => {
      history.push(`/album/${data.createAlbum}`);
      history.go(0);
    });
    return <Snackbar open={true} message={'New album created'} />;
  }

  if (error) return <Error />;

  return (
    <TopAppBarActionItem
      icon={disabled ? 'add' : 'add_circle_outline'}
      disabled={disabled ? true : false}
      onClick={() => handleUpdateAlbum(imageList)}
    />
  );
};

CreateAlbum.propTypes = {
  disabled: PropTypes.bool,
  imageList: PropTypes.array,
};

export default CreateAlbum;
