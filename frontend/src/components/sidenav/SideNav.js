import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import Divider from '@mui/material/Divider';
import Toolbar from '@mui/material/Toolbar';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListSubheader from '@mui/material/ListSubheader';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InsertPhotoIcon from '@mui/icons-material/InsertPhoto';
import SearchIcon from '@mui/icons-material/Search';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import StarIcon from '@mui/icons-material/Star';
import CollectionsBookmarkIcon from '@mui/icons-material/CollectionsBookmark';
import LibraryAddCheckIcon from '@mui/icons-material/LibraryAddCheck';
import DeleteIcon from '@mui/icons-material/Delete';

const sideNavItems1 = [
  { id: 'Photos', to: '/', icon: <InsertPhotoIcon /> },
  { id: 'Explore', to: '/explore', icon: <SearchIcon /> },
  { id: 'Sharing', to: '/sharing', icon: <PeopleAltIcon /> },
];

const sideNavItems2 = [
  { id: 'Favourites', to: '/favourites', icon: <StarIcon /> },
  { id: 'Albums', to: '/albums', icon: <CollectionsBookmarkIcon /> },
  { id: 'Utilities', to: '/utilities', icon: <LibraryAddCheckIcon /> },
  { id: 'Trash', to: '/trash', icon: <DeleteIcon /> },
];

const SideNav = ({ mobileOpen, handleDrawerToggle }) => {
  const drawerWidth = 240;
  const location = useLocation();

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {sideNavItems1.map((sn1) => (
          <Link
            to={sn1.to}
            key={sn1.to}
            onClick={() => handleDrawerToggle()}
            className="link"
          >
            <ListItem
              button
              key={sn1.id}
              selected={sn1.to === location.pathname}
            >
              <ListItemIcon>{sn1.icon}</ListItemIcon>
              <ListItemText primary={sn1.id} />
            </ListItem>
          </Link>
        ))}
      </List>
      <Divider />
      <List subheader={<ListSubheader>LIBRARY</ListSubheader>}>
        {sideNavItems2.map((sn2) => (
          <Link
            to={sn2.to}
            key={sn2.to}
            onClick={() => handleDrawerToggle()}
            className="link"
          >
            <ListItem
              button
              key={sn2.id}
              selected={sn2.to === location.pathname}
            >
              <ListItemIcon>{sn2.icon}</ListItemIcon>
              <ListItemText primary={sn2.id} />
            </ListItem>
          </Link>
        ))}
      </List>
    </div>
  );

  return (
    <>
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: drawerWidth,
          },
        }}
      >
        {drawer}
      </Drawer>
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': {
            boxSizing: 'border-box',
            width: drawerWidth,
          },
        }}
        open
      >
        {drawer}
      </Drawer>
    </>
  );
};

export default SideNav;
