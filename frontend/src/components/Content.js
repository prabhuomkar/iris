import React from 'react';
import PropTypes from 'prop-types';
import { Route, Switch } from 'react-router-dom';
import { DrawerAppContent } from '@rmwc/drawer';
import Photos from '../pages/Photos';
import Explore from '../pages/Explore';
import Sharing from '../pages/Sharing';
import SideNav from './SideNav';

const Content = (props) => {
  const { open } = props;
  return (
    <div>
      <SideNav open={open} />
      <DrawerAppContent>
        <Switch>
          <Route exact path="/" component={Photos} />
          <Route exact path="/explore" component={Explore} />
          <Route exact path="/sharing" component={Sharing} />
        </Switch>
      </DrawerAppContent>
    </div>
  );
};

Content.propTypes = {
  open: PropTypes.bool,
};

export default Content;
