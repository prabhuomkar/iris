import React from 'react';
import PropTypes from 'prop-types';
import {
  TopAppBar,
  TopAppBarRow,
  TopAppBarSection,
  TopAppBarTitle,
  TopAppBarFixedAdjust,
  TopAppBarNavigationIcon,
} from '@rmwc/top-app-bar';

import { NavLink } from 'react-router-dom';
import '@rmwc/top-app-bar/styles';

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
