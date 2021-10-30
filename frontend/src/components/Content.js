import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import { DrawerAppContent } from '@rmwc/drawer';
import Photos from '../pages/Photos';
import { Explore, People, Places, Things } from '../pages/explore';
import Upcoming from '../pages/Upcoming';
import SideNav from './SideNav';
import Photo from '../pages/Photo';
import Entity from '../pages/explore/Entity';
import Search from '../pages/Search';

const Content = (props) => {
  const { open } = props;
  return (
    <div>
      <SideNav open={open} />
      <DrawerAppContent>
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
          <Route path="/search" component={Search} />
          {/* static */}
          <Route exact path="/sharing" component={Upcoming} />
          <Route exact path="/favourites" component={Upcoming} />
          <Route exact path="/albums" component={Upcoming} />
          <Route exact path="/utilities" component={Upcoming} />
          <Route exact path="/archive" component={Upcoming} />
          <Route exact path="/trash" component={Upcoming} />
        </Switch>
      </DrawerAppContent>
    </div>
  );
};

Content.propTypes = {
  open: PropTypes.bool,
};

export default Content;
