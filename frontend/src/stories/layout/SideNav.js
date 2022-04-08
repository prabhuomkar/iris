import React from 'react';
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

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {sideNavItems1.map((sn1) => (
          <ListItem button key={sn1.id}>
            <ListItemIcon>{sn1.icon}</ListItemIcon>
            <ListItemText primary={sn1.id} />
          </ListItem>
        ))}
      </List>
      <Divider />
      <List subheader={<ListSubheader>LIBRARY</ListSubheader>}>
        {sideNavItems2.map((sn2) => (
          <ListItem button key={sn2.id}>
            <ListItemIcon>{sn2.icon}</ListItemIcon>
            <ListItemText primary={sn2.id} />
          </ListItem>
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
