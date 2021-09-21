import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { ExploreEntity } from '../../components';

const People = () => {
  const peopleData = [
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
    { image: '/avatar.jpg', label: 'People' },
  ];

  return (
    <>
      <Grid className="grid-cols" style={{ marginBottom: '10px' }}>
        <GridCell desktop={10} tablet={6} phone={3}>
          People
        </GridCell>
      </Grid>
      <Grid>
        <GridCell desktop={12} tablet={12} phone={12}>
          <ExploreEntity data={peopleData} />
        </GridCell>
      </Grid>
    </>
  );
};

export default People;
