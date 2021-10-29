import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import '@rmwc/grid/styles';

const Error = () => {
  return (
    <>
      <Grid>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
        <GridCell desktop={4} tablet={4} phone={4}>
          <img src="/warning.svg" width="100%" />
        </GridCell>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
      </Grid>
      <Grid>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
        <GridCell desktop={4} tablet={4} phone={4}>
          <center>Sorry, something went wrong.</center>
        </GridCell>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
      </Grid>
    </>
  );
};

export default Error;
