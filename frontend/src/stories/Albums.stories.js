import React from 'react';
import Albums from './components/Albums';

export default {
  title: 'Components/Albums',
  component: Albums,
};

export const Primary = () => {
  return <Albums />;
  {
    /*
    Name : Album
    Props:
      type: albums, favourites, trash
      data: album, favourites, trash api data
  */
  }
};
