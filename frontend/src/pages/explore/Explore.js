import React from 'react';
import { Link } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import '@rmwc/grid/styles';

const Explore = () => {
  return (
    <>
      <Grid>
        <GridCell span={11}>People</GridCell>
        <GridCell span={1}>
          <Link to="/explore/people" className="link-link">
            SEE ALL
          </Link>
        </GridCell>
      </Grid>
      <Grid>
        <GridCell span={11}>Places</GridCell>
        <GridCell span={1}>
          <Link to="/explore/places" className="link-link">
            SEE ALL
          </Link>
        </GridCell>
      </Grid>
      <Grid>
        <GridCell span={11}>Things</GridCell>
        <GridCell span={1}>
          <Link to="/explore/things" className="link-link">
            SEE ALL
          </Link>
        </GridCell>
      </Grid>
    </>
  );
};

export default Explore;
