import React from 'react';
import { useParams } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import '@rmwc/grid/styles';

const Album = () => {
  let { id } = useParams();
  return (
    <>
      <Grid>
        <GridCell span={12}>{id}</GridCell>
      </Grid>
    </>
  );
};

export default Album;
