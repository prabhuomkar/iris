import React from 'react';
import PropTypes from 'prop-types';
import { NavLink } from 'react-router-dom';
import { Drawer, DrawerSubtitle, DrawerContent } from '@rmwc/drawer';
import { List, ListItem, ListDivider } from '@rmwc/list';
import { Icon } from '@rmwc/icon';
import '@rmwc/drawer/styles';
import '@rmwc/list/styles';

const SideNav = (props) => {
  const { open } = props;

  const sideNavItems = [
    {
      subtitle: '',
      items: [
        { id: 'Photos', link_to: '', icon: 'image' },
        { id: 'Explore', link_to: 'explore', icon: 'search' },
        // { id: 'Sharing', link_to: 'sharing', icon: 'people' },
      ],
    },
    /*
    {
      subtitle: 'LIBRARY',
      items: [
        { id: 'Favourites', link_to: 'favourites', icon: 'star_rate' },
        { id: 'Albums', link_to: 'albums', icon: 'photo_album' },
        { id: 'Utilities', link_to: 'utilities', icon: 'filter_none' },
        { id: 'Archive', link_to: 'archive', icon: 'archive' },
        { id: 'Trash', link_to: 'trash', icon: 'delete' },
      ],
    },
    */
  ];

  return (
    <Drawer dismissible open={open} className="drawer">
      <DrawerContent className="drawer-content">
        <List>
          {sideNavItems.map((section) => (
            <div key={section.subtitle}>
              {section.subtitle ? (
                <DrawerSubtitle className="drawer-subtitle">
                  {section.subtitle}
                </DrawerSubtitle>
              ) : (
                <></>
              )}
              {section.items.map((item) => (
                <NavLink
                  key={item.link_to}
                  className="nav-link"
                  activeClassName="activated"
                  exact
                  to={`/${item.link_to}`}
                >
                  <ListItem className="list-item">
                    <Icon className="side-nav-icon" icon={item.icon} />
                    <span>{item.id}</span>
                  </ListItem>
                </NavLink>
              ))}
            </div>
          ))}
          <ListDivider />
        </List>
      </DrawerContent>
    </Drawer>
  );
};

SideNav.propTypes = {
  open: PropTypes.bool,
};

export default SideNav;
