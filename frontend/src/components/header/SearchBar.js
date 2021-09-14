import React from 'react';
import { TextField } from '@rmwc/textfield';
import '@rmwc/grid/styles';
import '@rmwc/textfield/styles';

const SearchBar = () => {
  return (
    <div className="search-bar-section">
      <TextField
        outlined
        className="search-bar"
        icon="search"
        placeholder="Search your photos"
      />
    </div>
  );
};

export default SearchBar;
