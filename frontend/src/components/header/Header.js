import React from 'react';
import PropTypes from 'prop-types';
import {
  TopAppBar,
  TopAppBarRow,
  TopAppBarSection,
  TopAppBarTitle,
  TopAppBarFixedAdjust,
  TopAppBarNavigationIcon,
  TopAppBarActionItem,
} from '@rmwc/top-app-bar';
import { NavLink } from 'react-router-dom';
import '@rmwc/top-app-bar/styles';
import SearchBar from './SearchBar';

const Header = ({ toggleSideNav }) => {
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
            <TopAppBarActionItem icon="help" />
            <TopAppBarActionItem icon="settings" />
          </TopAppBarSection>
        </TopAppBarRow>
      </TopAppBar>
      <TopAppBarFixedAdjust />
    </div>
  );
};

Header.propTypes = {
  toggleSideNav: PropTypes.func,
};

export default Header;
