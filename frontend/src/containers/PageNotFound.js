import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import '@rmwc/grid/styles';

const PageNotFound = () => {
  return (
    <>
      <Grid>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
        <GridCell desktop={4} tablet={4} phone={4}>
          <center>
            <img src="/404.svg" width="100%" />
            <br />
            <br />
            Page Not Found
          </center>
        </GridCell>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
      </Grid>
    </>
  );
};

export default PageNotFound;
