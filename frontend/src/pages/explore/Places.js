import React from 'react';
import { useLocation } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import { Loading, Error, ExploreEntity } from '../../components';

const GET_PLACES = gql`
  query getPlaces($entityType: String!) {
    entities(entityType: $entityType) {
      totalCount
      nodes {
        id
        name
        thumbnailUrl
      }
    }
  }
`;

const Places = () => {
  const location = useLocation();
  const type = location.pathname.split('/').pop();

  const { error: placesError, data: placesData } = useQuery(GET_PLACES, {
    variables: { entityType: 'places' },
    fetchPolicy: 'no-cache',
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
