import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import { ExploreEntity } from '../../components';

const GET_PLACES = gql`
  query GetPlaces($entityType: String!) {
    entities(entityType: $entityType, limit: 7) {
      totalCount
      nodes {
        id
        name
        imageUrl
      }
    }
  }
`;

const Places = () => {
  const { error: placesError, data: placesData } = useQuery(GET_PLACES, {
    variables: { entityType: 'places' },
  });

  if (placesError) return `Error! ${error.message}`;
  console.log(placesData);

  /*
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
  */

  return (
    <>
      {placesData && placesData.entities ? (
        <>
          <Grid className="grid-cols">
            <GridCell desktop={10} tablet={6} phone={3}>
              Places
            </GridCell>
          </Grid>
          <Grid>
            <GridCell desktop={12} tablet={12} phone={12}>
              <ExploreEntity data={placesData.entities.nodes} />
            </GridCell>
          </Grid>
        </>
      ) : (
        <>Loading...</>
      )}
    </>
  );
};

export default Places;
