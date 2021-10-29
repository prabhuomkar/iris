import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { TextField } from '@rmwc/textfield';
import '@rmwc/grid/styles';
import '@rmwc/textfield/styles';

const SearchBar = () => {
  const history = useHistory();
  const [search, setSearch] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    history.push(`/search?q=${search}`);
  };
  return (
    <div className="search-bar-section">
      <form onSubmit={handleSearch}>
        <TextField
          outlined
          className="search-bar"
          icon="search"
          value={search}
          placeholder="Search your photos"
          onChange={(e) => setSearch(e.target.value)}
        />
      </form>
    </div>
  );
};

export default SearchBar;
