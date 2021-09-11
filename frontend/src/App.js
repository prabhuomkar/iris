import React, { useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import Header from './components/header/Header';
import Content from './components/Content';
import './App.scss';

const App = () => {
  const [open, setOpen] = useState(true);
  const toggle = () => setOpen(!open);

  return (
    <BrowserRouter>
      <div className="App">
        <Header toggleSideNav={toggle} />
        <Content open={open} />
      </div>
    </BrowserRouter>
  );
};

export default App;
