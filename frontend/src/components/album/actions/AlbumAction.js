import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { MenuSurfaceAnchor, Menu, MenuItem } from '@rmwc/menu';
import { Icon } from '@rmwc/icon';
import DeleteAlbum from './DeleteAlbum';
import RenameAlbum from './RenameAlbum';
import '@rmwc/menu/styles';

const DeleteAction = ({ openDelete, setOpenDelete, albumId, albumName }) => {
  return (
    <DeleteAlbum
      openDelete={openDelete}
      setOpenDelete={setOpenDelete}
      albumId={albumId}
      albumName={albumName}
    />
  );
};

const AlbumAction = ({ albumId, albumName }) => {
  const [open, setOpen] = useState(false);
  const [openDelete, setOpenDelete] = useState(false);
  const [openRename, setOpenRename] = useState(false);

  return (
    <>
      <MenuSurfaceAnchor>
        <Menu
          open={open}
          onClose={() => setOpen(false)}
          style={{ width: '160px' }}
        >
          <MenuItem onClick={() => setOpenRename(true)}>Rename album</MenuItem>
          <MenuItem onClick={() => setOpenDelete(true)}>Delete</MenuItem>
        </Menu>
        <Icon
          icon={{
            icon: 'more_vert',
            size: 'medium',
          }}
          style={{ color: '#fff' }}
          onClick={() => setOpen(!open)}
        />
      </MenuSurfaceAnchor>
      <DeleteAction
        openDelete={openDelete}
        setOpenDelete={setOpenDelete}
        albumId={albumId}
        albumName={albumName}
      />
      <RenameAlbum openRename={openRename} setOpenRename={setOpenRename} />
    </>
  );
};

DeleteAction.propTypes = {
  openDelete: PropTypes.bool,
  setOpenDelete: PropTypes.func,
  albumId: PropTypes.string,
  albumName: PropTypes.string,
};

AlbumAction.propTypes = {
  albumId: PropTypes.string,
  albumName: PropTypes.string,
};

export default AlbumAction;
