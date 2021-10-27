import React from 'react';
import { Link } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import { gql, useQuery } from '@apollo/client';
import { ExploreEntityList } from '../../components';
import '@rmwc/grid/styles';

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

const GET_THINGS = gql`
  query GetThings($entityType: String!) {
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

/*
const peopleList = [
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
  '/avatar.jpg',
];

const placesList = [
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
  '/places.jpg',
];

const thingsList = [
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
  '/things.jpeg',
];
*/

const Explore = () => {
  const { error: placesError, data: placesData } = useQuery(GET_PLACES, {
    variables: { entityType: 'places' },
  });

  const { error: thingsError, data: thingsData } = useQuery(GET_THINGS, {
    variables: { entityType: 'things' },
  });

  if (placesError) return `Error! ${error.message}`;
  if (thingsError) return `Error! ${error.message}`;
  console.log(placesData);
  console.log(thingsData);

  return (
    <>
      {placesData &&
      placesData.entities &&
      thingsData &&
      thingsData.entities ? (
        <>
          {/*
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
              <ExploreEntityList type="PeopleList" data={peopleList} />
            </GridCell>
          </Grid>
          */}
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
                type="PlacesList"
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
                type="ThingsList"
                data={thingsData.entities.nodes}
              />
            </GridCell>
          </Grid>
        </>
      ) : (
        <>Loading...</>
      )}
    </>
  );
};

export default Explore;
