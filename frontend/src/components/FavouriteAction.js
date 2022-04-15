import React, { useState, useEffect } from 'react';
import { gql, useMutation } from '@apollo/client';
import PropTypes from 'prop-types';
import { Icon } from '@rmwc/icon';

const FAVOURITE = gql`
  mutation favourite($id: String!, $type: String!) {
    favourite(id: $id, type: $type)
  }
`;

const FavouriteAction = ({ liked, id }) => {
  const [fav, setFav] = useState(false);

  useEffect(() => {
    setFav(liked);
  }, [liked]);

  const [favourite, { loading: favLoading }] =
    useMutation(FAVOURITE);

  const handleFavButtonClick = (photoId, action) => {
    favourite({
      variables: { id: photoId, type: action },
    });
    setFav(!fav);
  };

  if (favLoading) return null;

  return (
    <Icon
      icon={{ icon: fav ? 'star' : 'star_outline', size: 'large' }}
      style={{ color: '#fff', cursor: 'pointer' }}
      onClick={() => handleFavButtonClick(id, fav ? 'remove' : 'add')}
    />
  );
};

FavouriteAction.propTypes = {
  liked: PropTypes.bool,
  id: PropTypes.string,
};

export default FavouriteAction;
