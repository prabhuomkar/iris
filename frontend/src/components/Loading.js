import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { LinearProgress } from '@rmwc/linear-progress';
import '@rmwc/linear-progress/styles';
import '@rmwc/grid/styles';

const Loading = () => {
  return (
    <>
      <Grid>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
        <GridCell desktop={4} tablet={4} phone={4}>
          <img src="/images.svg" width="100%" />
        </GridCell>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
      </Grid>
      <Grid>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
        <GridCell desktop={4} tablet={4} phone={4}>
          <LinearProgress />
        </GridCell>
        <GridCell desktop={4} tablet={4} phone={4}></GridCell>
      </Grid>
    </>
  );
};

export default Loading;
