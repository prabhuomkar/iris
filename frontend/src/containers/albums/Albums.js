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
import { Loading, Error, AlbumAction } from '../../components';
import './style.scss';

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
  const { error, data } = useQuery(GET_ALBUMS, {
    fetchPolicy: 'no-cache',
  });
  if (error) return <Error />;
  let history = useHistory();

  return (
    <>
      {data && data.albums && data.albums.nodes ? (
        <>
          {data.albums && data.albums.totalCount === 0 ? (
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
                    {data.albums.nodes.map((album) => (
                      <ImageListItem key={album.id} className="image-list-item">
                        <div className="image-list-item-container">
                          <ImageListImageAspectContainer>
                            <div className="image-aspect-container">
                              <AlbumAction
                                albumId={album?.id}
                                albumName={album?.name}
                              />
                            </div>
                            {album.mediaItems?.totalCount !== 0 ? (
                              <ImageListImage
                                src={`${album.previewUrl}?width=200&height=200`}
                                className="image-list-image"
                                onClick={() =>
                                  history.push(`/album/${album.id}`)
                                }
                              />
                            ) : (
                              <ImageListImage
                                className="image-list-image"
                                onClick={() =>
                                  history.push(`/album/${album.id}`)
                                }
                              />
                            )}
                          </ImageListImageAspectContainer>
                        </div>
                        <ImageListSupporting className="album-list-info">
                          <ImageListLabel>
                            {album.name}
                            <div>
                              <small style={{ color: '#424242' }}>
                                {album.mediaItems?.totalCount} items
                              </small>
                            </div>
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
