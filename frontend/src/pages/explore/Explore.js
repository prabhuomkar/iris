import React from 'react';
import { Link } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import '@rmwc/grid/styles';

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
    </>
  );
};

export default Explore;
