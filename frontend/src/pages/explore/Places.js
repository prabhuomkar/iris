import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { ExploreEntity } from '../../components';

const Places = () => {
  const placesData = [
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
    { image: '/places.jpg', label: 'Places' },
  ];

  return (
    <>
      <Grid className="grid-cols" style={{ marginBottom: '10px' }}>
        <GridCell desktop={10} tablet={6} phone={3}>
          Places
        </GridCell>
      </Grid>
      <Grid>
        <GridCell desktop={12} tablet={12} phone={12}>
          <ExploreEntity data={placesData} />
        </GridCell>
      </Grid>
    </>
  );
};

export default Places;
