import React from 'react';
import { useLocation } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import { Loading, Error, ExploreEntity } from '../../components';

const GET_PEOPLE = gql`
  query getPeople($entityType: String!) {
    entities(entityType: $entityType) {
      totalCount
      nodes {
        id
        name
        previewUrl
      }
    }
  }
`;

const People = () => {
  const location = useLocation();
  const type = location.pathname.split('/').pop();

  const { error: peopleError, data: peopleData } = useQuery(GET_PEOPLE, {
    variables: { entityType: 'people' },
    fetchPolicy: 'no-cache',
  });

  if (peopleError) return <Error />;

  return (
    <>
      {peopleData && peopleData.entities ? (
        <>
          <Grid className="grid-cols">
            <GridCell desktop={10} tablet={6} phone={3}>
              People
            </GridCell>
          </Grid>
          <Grid>
            <GridCell desktop={12} tablet={12} phone={12}>
              <ExploreEntity type={type} data={peopleData.entities.nodes} />
            </GridCell>
          </Grid>
        </>
      ) : (
        <Loading />
      )}
    </>
  );
};

export default People;
