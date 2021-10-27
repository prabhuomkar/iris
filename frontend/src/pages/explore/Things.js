import React from 'react';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import { ExploreEntity } from '../../components';

const GET_THINGS = gql`
  query GetThings($entityType: String!) {
    entities(entityType: $entityType) {
      totalCount
      nodes {
        id
        name
        imageUrl
      }
    }
  }
`;

const Things = () => {
  const { error: thingsError, data: thingsData } = useQuery(GET_THINGS, {
    variables: { entityType: 'things' },
  });

  if (thingsError) return `Error! ${error.message}`;
  //console.log(thingsData);

  /*
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
  */

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
              <ExploreEntity data={thingsData.entities.nodes} />
            </GridCell>
          </Grid>
        </>
      ) : (
        <>Loading...</>
      )}
    </>
  );
};

export default Things;
