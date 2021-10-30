import React from 'react';
import { Link } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import {
  Loading,
  Error,
  ExploreEntityList,
  ExplorePeopleList,
} from '../../components';
import '@rmwc/grid/styles';

const GET_PEOPLE = gql`
  query getPeople($entityType: String!) {
    entities(entityType: $entityType, limit: 8) {
      totalCount
      nodes {
        id
        name
        imageUrl
      }
    }
  }
`;

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
  const { error: peopleError, data: peopleData } = useQuery(GET_PEOPLE, {
    variables: { entityType: 'people' },
    fetchPolicy: 'no-cache',
  });

  const { error: placesError, data: placesData } = useQuery(GET_PLACES, {
    variables: { entityType: 'places' },
    fetchPolicy: 'no-cache',
  });

  const { error: thingsError, data: thingsData } = useQuery(GET_THINGS, {
    variables: { entityType: 'things' },
    fetchPolicy: 'no-cache',
  });

  if (placesError || thingsError || peopleError) return <Error />;

  return (
    <>
      {peopleData &&
      peopleData.entities &&
      placesData &&
      placesData.entities &&
      thingsData &&
      thingsData.entities ? (
        <>
          {peopleData.entities.totalCount === 0 &&
          placesData.entities.totalCount === 0 &&
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
                  People
                </GridCell>
                <GridCell desktop={2} tablet={2} phone={1}>
                  <Link to="/explore/people" className="link">
                    SEE ALL
                  </Link>
                </GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={12} tablet={12} phone={12}>
                  <ExplorePeopleList
                    type="people"
                    data={peopleData.entities.nodes}
                  />
                </GridCell>
              </Grid>
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
