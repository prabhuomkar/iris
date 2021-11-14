import React from 'react';
import { gql, useMutation } from '@apollo/client';
import { useHistory } from 'react-router-dom';
import PropTypes from 'prop-types';
import { Snackbar } from '@rmwc/snackbar';
import '@rmwc/snackbar/styles';
import { Icon } from '@rmwc/icon';

const DELETE_ITEM = gql`
  mutation deleteItem($id: String!, $type: String!) {
    delete(id: $id, type: $type)
  }
`;

const DeleteAction = ({ deleted, id }) => {
  const history = useHistory();
  const [deleteItem, { data: delData, loading: delLoading }] =
    useMutation(DELETE_ITEM);

  const handleDelButtonClick = (photoId, action) => {
    deleteItem({
      variables: { id: photoId, type: action },
    });
  };

  if (delLoading)
    return (
      <Snackbar
        open={true}
        message={deleted ? 'Restoring...' : 'Moving to Trash...'}
      />
    );

  if (delData && delData.delete) {
    setTimeout(() => {
      history.push('/');
    }, 2000);

    return (
      <Snackbar open={true} message={deleted ? 'Restored' : 'Moved to Trash'} />
    );
  }

  return (
    <Icon
      icon={{ icon: deleted ? 'restore' : 'delete_outline', size: 'large' }}
      style={{ color: '#fff', cursor: 'pointer' }}
      onClick={() => handleDelButtonClick(id, deleted ? 'remove' : 'add')}
    />
  );
};

DeleteAction.propTypes = {
  deleted: PropTypes.bool,
  id: PropTypes.string,
};

export default DeleteAction;
