import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import { Loading, Error, ExploreEntity } from '../../components';

const GET_THINGS = gql`
  query getThings($entityType: String!) {
    entities(entityType: $entityType) {
      totalCount
      nodes {
        id
        name
        displayMediaItem {
          imageUrl
        }
      }
    }
  }
`;

const Things = () => {
  const url = window.location.pathname;
  const type = url.split('/').pop();
  const { error: thingsError, data: thingsData } = useQuery(GET_THINGS, {
    variables: { entityType: 'things' },
    fetchPolicy: 'no-cache',
  });

  if (thingsError) return <Error />;

  return (
    <>
      {thingsData && thingsData.entities ? (
        <>
          <Grid className="grid-cols">
            <GridCell desktop={10} tablet={6} phone={3}>
              Things
            </GridCell>
          </Grid>
          <Grid>
            <GridCell desktop={12} tablet={12} phone={12}>
              <ExploreEntity type={type} data={thingsData.entities.nodes} />
            </GridCell>
          </Grid>
        </>
      ) : (
        <Loading />
      )}
    </>
  );
};

export default Things;
