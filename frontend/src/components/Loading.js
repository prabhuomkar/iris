import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { CircularProgress } from '@rmwc/circular-progress';
import '@rmwc/circular-progress/styles';
import '@rmwc/grid/styles';

const Loading = () => {
  return (
    <>
      <Grid>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
        <GridCell desktop={4} tablet={4} phone={4}>
          <center>
            <CircularProgress size="xlarge" />
            <br />
            <span>Loading...</span>
          </center>
        </GridCell>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
      </Grid>
    </>
  );
};

export default Loading;
