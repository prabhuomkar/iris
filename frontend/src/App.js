import React, { useState, createContext } from 'react';
import { createUploadLink } from 'apollo-upload-client';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import { ThemeProvider } from '@rmwc/theme';
import { BrowserRouter } from 'react-router-dom';
import { Header, Content } from './components';
import SideNav from './components/SideNav';
import { DrawerAppContent } from '@rmwc/drawer';
import '@rmwc/theme/styles';
import './App.scss';
export const AlbumsContext = createContext();

const link = createUploadLink({ uri: process.env.REACT_APP_API_URL });
const client = new ApolloClient({
  link,
  cache: new InMemoryCache(),
});

const App = () => {
  const [open, setOpen] = useState(true);
  const toggle = () => setOpen(!open);

  const [imageList, setImageList] = useState([]);
  const [removeImageList, setRemoveImageList] = useState([]);
  const [addImageList, setAddImageList] = useState([]);

  return (
    <ApolloProvider client={client}>
      <div className="App">
        <AlbumsContext.Provider
          value={{
            createAlbum: [imageList, setImageList],
            removePhotos: [removeImageList, setRemoveImageList],
            addPhotos: [addImageList, setAddImageList],
          }}
        >
          <ThemeProvider
            options={{
              primary: '#812ce5',
              secondary: '#ffffff',
              onPrimary: '#812ce5',
              textPrimaryOnBackground: '#000',
            }}
          >
            <BrowserRouter>
              <Header toggleSideNav={toggle} />
              <SideNav open={open} />
              <DrawerAppContent>
                <Content />
              </DrawerAppContent>
            </BrowserRouter>
          </ThemeProvider>
        </AlbumsContext.Provider>
      </div>
    </ApolloProvider>
  );
};

export default App;
