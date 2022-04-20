import React from 'react';
import { useHistory } from 'react-router-dom';
import { gql, useQuery } from '@apollo/client';
import { Grid, GridCell } from '@rmwc/grid';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListLabel,
  ImageListSupporting,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import { Loading, Error } from '../../components';

const GET_ALBUMS = gql`
  query getAlbums {
    albums {
      totalCount
      nodes {
        id
        name
        previewUrl
        mediaItems {
          totalCount
        }
      }
    }
  }
`;

const Albums = () => {
  const { error: albumsError, data: albumsData } = useQuery(GET_ALBUMS, {
    fetchPolicy: 'no-cache',
  });
  if (albumsError) return <Error />;

  let history = useHistory();
  const styleFav = {
    radius: '4px',
    width: '180px',
    margin: '0px 6px 8px 6px',
  };

  return (
    <>
      {albumsData && albumsData.albums && albumsData.albums.nodes ? (
        <>
          {albumsData.albums && albumsData.albums.totalCount === 0 ? (
            <>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <center>
                    <img src="/albums.svg" width="100%" />
                    <br />
                    <br />
                    You have not created any albums yet!
                  </center>
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
            </>
          ) : (
            <>
              <Grid className="grid-cols">
                <GridCell desktop={10} tablet={6} phone={3}>
                  Albums
                </GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={12} tablet={12} phone={12}>
                  <ImageList>
                    {albumsData.albums.nodes.map((album) => (
                      <ImageListItem key={album.id} style={styleFav}>
                        <ImageListImageAspectContainer>
                          {album.mediaItems?.totalCount !== 0 ? (
                            <ImageListImage
                              src={`${album.previewUrl}?width=200&height=200`}
                              style={{
                                cursor: 'pointer',
                                borderRadius: '4px',
                              }}
                              onClick={() => history.push(`/album/${album.id}`)}
                            />
                          ) : (
                            <ImageListImage
                              style={{
                                cursor: 'pointer',
                                borderRadius: '4px',
                              }}
                              onClick={() => history.push(`/album/${album.id}`)}
                            />
                          )}
                        </ImageListImageAspectContainer>
                        <ImageListSupporting className="album-list-info">
                          <ImageListLabel>
                            {album.name}
                            <br />
                            <small style={{ color: '#424242' }}>
                              {album.mediaItems?.totalCount} items
                            </small>
                          </ImageListLabel>
                        </ImageListSupporting>
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

export default Albums;
