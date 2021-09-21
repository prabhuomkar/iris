import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { ExploreEntity } from '../../components';

const Things = () => {
  const thingsData = [
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
    { image: '/things.jpeg', label: 'Things' },
  ];

  return (
    <>
      <Grid className="grid-cols" style={{ marginBottom: '10px' }}>
        <GridCell desktop={10} tablet={6} phone={3}>
          Things
        </GridCell>
      </Grid>
      <Grid>
        <GridCell desktop={12} tablet={12} phone={12}>
          <ExploreEntity data={thingsData} />
        </GridCell>
      </Grid>
    </>
  );
};

export default Things;
