import React, { useContext } from 'react';
import { useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';
import {
  TopAppBar,
  TopAppBarRow,
  TopAppBarSection,
  TopAppBarTitle,
  TopAppBarFixedAdjust,
  TopAppBarNavigationIcon,
} from '@rmwc/top-app-bar';
import '@rmwc/top-app-bar/styles';
import { NavLink } from 'react-router-dom';
import SearchBar from './SearchBar';
import Upload from './Upload';
import CreateAlbum from './CreateAlbum';
import UpdateAlbum from '../UpdateAlbum';
import { AlbumsContext } from '../../App';

const Header = ({ toggleSideNav }) => {
  const location = useLocation();
  const albumId = location.pathname.split('/').pop();
  const { createAlbum, removePhotos } = useContext(AlbumsContext);
  const [removeImageList] = removePhotos;
  const [imageList] = createAlbum;

  return (
    <div>
      <TopAppBar className="top-app-bar" fixed>
        <TopAppBarRow>
          <TopAppBarSection>
            <TopAppBarNavigationIcon icon="menu" onClick={toggleSideNav} />
            <TopAppBarTitle>
              <NavLink exact to="/" className="header-title">
                <span>iris</span>
              </NavLink>
            </TopAppBarTitle>
          </TopAppBarSection>
          <TopAppBarSection>
            <SearchBar />
          </TopAppBarSection>
          <TopAppBarSection alignEnd>
            <UpdateAlbum
              removeImageList={removeImageList}
              disabled={removeImageList.length === 0}
              albumId={albumId}
            />
            <CreateAlbum
              imageList={imageList}
              disabled={imageList.length === 0}
            />
            &nbsp;&nbsp;
            <Upload />
            {/*
            <TopAppBarActionItem icon="help" />
            <TopAppBarActionItem icon="settings" />
            */}
          </TopAppBarSection>
        </TopAppBarRow>
      </TopAppBar>
      <TopAppBarFixedAdjust />
    </div>
  );
};

Header.propTypes = {
  toggleSideNav: PropTypes.func,
  showAdd: PropTypes.bool,
};

export default Header;
