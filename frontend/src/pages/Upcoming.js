import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import '@rmwc/grid/styles';

const Upcoming = () => {
  return (
    <>
      <Grid>
        <GridCell span={12}>
          <img src="/pytorch2021.png" width="100%" />
        </GridCell>
      </Grid>
      <Grid>
        <GridCell span={12}>
          <center>
            <h2>
              <p>This is out of scope for Hackathon Submission.</p>
              <p>This feature will be released in December 2021 version.</p>
            </h2>
          </center>
        </GridCell>
      </Grid>
    </>
  );
};

export default Upcoming;
