import React, { useState } from 'react';
import { ThemeProvider } from '@rmwc/theme';
import { BrowserRouter } from 'react-router-dom';
import { createUploadLink } from 'apollo-upload-client';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import { Header, Content } from './components';
import '@rmwc/theme/styles';
import './App.scss';

const App = () => {
  const link = createUploadLink({ uri: process.env.REACT_APP_API_URL });
  const client = new ApolloClient({
    link,
    cache: new InMemoryCache(),
  });
  const [open, setOpen] = useState(true);
  const toggle = () => setOpen(!open);

  return (
    <ApolloProvider client={client}>
      <ThemeProvider
        options={{
          primary: '#812ce5',
          secondary: '#ffffff',
          onPrimary: '#812ce5',
          textPrimaryOnBackground: '#000',
        }}
      >
        <BrowserRouter>
          <div className="App">
            <Header toggleSideNav={toggle} />
            <Content open={open} />
          </div>
        </BrowserRouter>
      </ThemeProvider>
    </ApolloProvider>
  );
};

export default App;
