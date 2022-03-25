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

const drawerItems1 = [
  { id: 'Photos', link_to: '', icon: <InsertPhotoIcon /> },
  { id: 'Explore', link_to: 'explore', icon: <SearchIcon /> },
  { id: 'Sharing', link_to: 'sharing', icon: <PeopleAltIcon /> },
];

const drawerItems2 = [
  { id: 'Favourites', link_to: 'favourites', icon: <StarIcon /> },
  { id: 'Albums', link_to: 'albums', icon: <CollectionsBookmarkIcon /> },
  { id: 'Utilities', link_to: 'utilities', icon: <LibraryAddCheckIcon /> },
  { id: 'Trash', link_to: 'trash', icon: <DeleteIcon /> },
];

const IDrawer = ({ mobileOpen, handleDrawerToggle }) => {
  const drawerWidth = 240;

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {drawerItems1.map((dr1) => (
          <ListItem button key={dr1.id}>
            <ListItemIcon>{dr1.icon}</ListItemIcon>
            <ListItemText primary={dr1.id} />
          </ListItem>
        ))}
      </List>
      <Divider />
      <List subheader={<ListSubheader>LIBRARY</ListSubheader>}>
        {drawerItems2.map((dr2) => (
          <ListItem button key={dr2.id}>
            <ListItemIcon>{dr2.icon}</ListItemIcon>
            <ListItemText primary={dr2.id} />
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

export default IDrawer;
