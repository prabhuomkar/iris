import React, { useState, useEffect } from 'react';
import { gql, useMutation } from '@apollo/client';
import PropTypes from 'prop-types';
import { Icon } from '@rmwc/icon';

const UPDATE_FAVOURITE = gql`
  mutation updateFavourite($id: String!, $type: String!) {
    updateFavourite(id: $id, type: $type)
  }
`;

const FavouriteAction = ({ liked, id }) => {
  const [fav, setFav] = useState(false);

  useEffect(() => {
    setFav(liked);
  }, [liked]);

  const [updateFavourite, { loading: favLoading }] =
    useMutation(UPDATE_FAVOURITE);

  const handleAddFav = (photoId) => {
    updateFavourite({
      variables: { id: photoId, type: 'add' },
    });
    setFav(!fav);
  };

  const handleRemoveFav = (photoId) => {
    updateFavourite({
      variables: { id: photoId, type: 'remove' },
    });
    setFav(!fav);
  };

  if (favLoading) return null;

  return (
    <>
      {fav ? (
        <Icon
          icon={{ icon: 'star', size: 'large' }}
          style={{ color: '#fff', cursor: 'pointer' }}
          onClick={() => handleRemoveFav(id)}
        />
      ) : (
        <Icon
          icon={{ icon: 'star_outline', size: 'large' }}
          style={{ color: '#fff', cursor: 'pointer' }}
          onClick={() => handleAddFav(id)}
        />
      )}
    </>
  );
};

FavouriteAction.propTypes = {
  liked: PropTypes.bool,
  id: PropTypes.string,
};

export default FavouriteAction;
