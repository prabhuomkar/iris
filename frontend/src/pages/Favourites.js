import React from 'react';
import { useHistory } from 'react-router-dom';
import { gql, useQuery } from '@apollo/client';
import { Grid, GridCell } from '@rmwc/grid';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import { Loading, Error } from '../components';

const GET_FAVOURITES = gql`
  query getFavourites {
    favourites {
      totalCount
      nodes {
        id
        imageUrl
      }
    }
  }
`;

const Favourites = () => {
  const { error: favError, data: favData } = useQuery(GET_FAVOURITES, {
    fetchPolicy: 'no-cache',
  });
  if (favError) return <Error />;

  let history = useHistory();
  const styleFav = {
    radius: '4px',
    width: '180px',
    margin: '0px 6px 8px 6px',
  };

  return (
    <>
      {favData && favData.favourites && favData.favourites.nodes ? (
        <>
          {favData.favourites && favData.favourites.totalCount === 0 ? (
            <>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <center>
                    <img src="/favourites.svg" width="100%" />
                    <br />
                    You have no favourite photos yet!
                  </center>
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
            </>
          ) : (
            <>
              <Grid className="grid-cols">
                <GridCell desktop={10} tablet={6} phone={3}>
                  Favourites
                </GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={12} tablet={12} phone={12}>
                  <ImageList>
                    {favData.favourites.nodes.map((src) => (
                      <ImageListItem key={src.id} style={styleFav}>
                        <ImageListImageAspectContainer>
                          <ImageListImage
                            src={`${src.imageUrl}?width=200&height=200`}
                            style={{ cursor: 'pointer', borderRadius: '4px' }}
                            onClick={() => history.push(`/photo/${src.id}`)}
                          />
                        </ImageListImageAspectContainer>
                      </ImageListItem>
                    ))}
                  </ImageList>
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

export default Favourites;
