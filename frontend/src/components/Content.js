import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import { DrawerAppContent } from '@rmwc/drawer';
import Photos from '../pages/Photos';
import { Explore, People, Places, Things } from '../pages/explore';
import Sharing from '../pages/Sharing';
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
          <Route exact path="/explore/places/:id" component={Entity} />
          <Route exact path="/explore/things/:id" component={Entity} />
          <Route exact path="/sharing" component={Sharing} />
          <Route exact path="/photo/:id" component={Photo} />
          <Route path="/search" component={Search} />
        </Switch>
      </DrawerAppContent>
    </div>
  );
};

Content.propTypes = {
  open: PropTypes.bool,
};

export default Content;
