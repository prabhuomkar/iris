import React, { useState, createContext } from 'react';
import { ThemeProvider } from '@rmwc/theme';
import { BrowserRouter } from 'react-router-dom';
import { DrawerAppContent } from '@rmwc/drawer';
import { Header, Content } from './components';
import SideNav from './components/SideNav';
import '@rmwc/theme/styles';
import './App.scss';
export const CreateAlbumContext = createContext();

const App = () => {
  const [open, setOpen] = useState(true);
  const toggle = () => setOpen(!open);

  const [imageList, setImageList] = useState([]);

  return (
    <ThemeProvider
      options={{
        primary: '#812ce5',
        secondary: '#ffffff',
        onPrimary: '#812ce5',
        textPrimaryOnBackground: '#000',
      }}
    >
      <CreateAlbumContext.Provider value={{ imageList, setImageList }}>
        <BrowserRouter>
          <div className="App">
            <Header toggleSideNav={toggle} />
            <SideNav open={open} />
            <DrawerAppContent>
              <Content />
            </DrawerAppContent>
          </div>
        </BrowserRouter>
      </CreateAlbumContext.Provider>
    </ThemeProvider>
  );
};

export default App;
