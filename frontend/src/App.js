import React, { useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import { Header, Content } from './components';
import './App.scss';

const App = () => {
  const client = new ApolloClient({
    uri: process.env.REACT_APP_API_URL,
    cache: new InMemoryCache(),
  });
  const [open, setOpen] = useState(true);
  const toggle = () => setOpen(!open);

  return (
    <ApolloProvider client={client}>
      <BrowserRouter>
        <div className="App">
          <Header toggleSideNav={toggle} />
          <Content open={open} />
        </div>
      </BrowserRouter>
    </ApolloProvider>
  );
};

export default App;
