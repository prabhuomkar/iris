import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import { Loading, Error, ExploreEntity } from '../../components';

const GET_PLACES = gql`
  query getPlaces($entityType: String!) {
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
  const url = window.location.pathname;
  const type = url.split('/').pop();

  const { error: placesError, data: placesData } = useQuery(GET_PLACES, {
    variables: { entityType: 'places' },
  });

  if (placesError) return <Error />;

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
              <ExploreEntity type={type} data={placesData.entities.nodes} />
            </GridCell>
          </Grid>
        </>
      ) : (
        <Loading />
      )}
    </>
  );
};

export default Places;
