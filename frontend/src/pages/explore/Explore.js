import React from 'react';
import { Link } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import { ExploreImageList } from '../../components';
import '@rmwc/grid/styles';

const peopleList = [
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
];

const placesList = [
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
];

const thingsList = [
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
];

const Explore = () => {
  return (
    <>
      <Grid className="grid-cols">
        <GridCell desktop={10} tablet={6} phone={3}>
          People
        </GridCell>
        <GridCell desktop={2} tablet={2} phone={1}>
          <Link to="/explore/people" className="link">
            SEE ALL
          </Link>
        </GridCell>
      </Grid>
      <Grid>
        <GridCell desktop={12} tablet={12} phone={12}>
          <ExploreImageList
            listRadius="50%"
            listWidth="10%"
            listMargin="0px 6px 6px 6px"
            data={peopleList}
          />
        </GridCell>
      </Grid>
      <Grid className="grid-cols">
        <GridCell desktop={10} tablet={6} phone={3}>
          Places
        </GridCell>
        <GridCell desktop={2} tablet={2} phone={1}>
          <Link to="/explore/places" className="link">
            SEE ALL
          </Link>
        </GridCell>
      </Grid>
      <Grid>
        <GridCell desktop={12} tablet={12} phone={12}>
          <ExploreImageList
            listRadius="6px"
            listWidth="13%"
            listMargin="0px 6px 12px 6px"
            data={placesList}
          />
        </GridCell>
      </Grid>
      <Grid className="grid-cols">
        <GridCell desktop={10} tablet={6} phone={3}>
          Things
        </GridCell>
        <GridCell desktop={2} tablet={2} phone={1}>
          <Link to="/explore/things" className="link">
            SEE ALL
          </Link>
        </GridCell>
      </Grid>
      <Grid>
        <GridCell desktop={12} tablet={12} phone={12}>
          <ExploreImageList
            listRadius="6px"
            listWidth="13%"
            listMargin="0px 6px 12px 6px"
            data={thingsList}
          />
        </GridCell>
      </Grid>
    </>
  );
};

export default Explore;
