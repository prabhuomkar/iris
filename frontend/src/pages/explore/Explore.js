import React from 'react';
import { Link } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import { Loading, Error, ExploreEntityList } from '../../components';
import '@rmwc/grid/styles';

const GET_PLACES = gql`
  query getPlaces($entityType: String!) {
    entities(entityType: $entityType, limit: 6) {
      totalCount
      nodes {
        id
        name
        imageUrl
      }
    }
  }
`;

const GET_THINGS = gql`
  query getThings($entityType: String!) {
    entities(entityType: $entityType, limit: 6) {
      totalCount
      nodes {
        id
        name
        imageUrl
      }
    }
  }
`;

const Explore = () => {
  const { error: placesError, data: placesData } = useQuery(GET_PLACES, {
    variables: { entityType: 'places' },
  });

  const { error: thingsError, data: thingsData } = useQuery(GET_THINGS, {
    variables: { entityType: 'things' },
  });

  if (placesError || thingsError) return <Error />;

  return (
    <>
      {placesData &&
      placesData.entities &&
      thingsData &&
      thingsData.entities ? (
        <>
          {placesData.entities.totalCount === 0 &&
          thingsData.entities.totalCount === 0 ? (
            <>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <img src="/explore.svg" width="100%" />
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <center>
                    Upload your photos to iris! so you can find them faster
                  </center>
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
            </>
          ) : (
            <>
              <Grid className="grid-cols">
                <GridCell desktop={10} tablet={6} phone={3}>
                  Places
                </GridCell>
                <GridCell desktop={2} tablet={2} phone={1}>
                  <Link to="/explore/places" className="link">
                    SEE ALL
                  </Link>
                </GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={12} tablet={12} phone={12}>
                  <ExploreEntityList
                    type="places"
                    data={placesData.entities.nodes}
                  />
                </GridCell>
              </Grid>
              <Grid className="grid-cols">
                <GridCell desktop={10} tablet={6} phone={3}>
                  Things
                </GridCell>
                <GridCell desktop={2} tablet={2} phone={1}>
                  <Link to="/explore/things" className="link">
                    SEE ALL
                  </Link>
                </GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={12} tablet={12} phone={12}>
                  <ExploreEntityList
                    type="things"
                    data={thingsData.entities.nodes}
                  />
                </GridCell>
              </Grid>
            </>
          )}
        </>
      ) : (
        <Loading />
      )}
    </>
  );
};

export default Explore;
