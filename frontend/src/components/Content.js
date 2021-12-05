import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import {
  Photo,
  Photos,
  Search,
  Upcoming,
  Favourites,
  Trash,
  Albums,
  Album,
} from '../pages';
import { Explore, People, Places, Things, Entity } from '../pages/explore';

const Content = () => {
  return (
    <>
      <Switch>
        <Route exact path="/" component={Photos} />
        <Route exact path="/explore" component={Explore} />
        <Route exact path="/explore/people" component={People} />
        <Route exact path="/explore/places" component={Places} />
        <Route exact path="/explore/things" component={Things} />
        <Route exact path="/explore/people/:id" component={Entity} />
        <Route exact path="/explore/places/:id" component={Entity} />
        <Route exact path="/explore/things/:id" component={Entity} />
        <Route exact path="/photo/:id" component={Photo} />
        <Route exact path="/favourites" component={Favourites} />
        <Route exact path="/albums" component={Albums} />
        <Route exact path="/album/:id" component={Album} />
        <Route path="/search" component={Search} />
        {/* static */}
        <Route exact path="/sharing" component={Upcoming} />
        <Route exact path="/utilities" component={Upcoming} />
        <Route exact path="/archive" component={Upcoming} />
        <Route exact path="/trash" component={Trash} />
      </Switch>
    </>
  );
};

Content.propTypes = {
  open: PropTypes.bool,
  setData: PropTypes.func,
};

export default Content;
