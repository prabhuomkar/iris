import React from 'react';
import moment from 'moment';
import { Link } from 'react-router-dom';
import { gql, useQuery } from '@apollo/client';
import { Grid, GridCell } from '@rmwc/grid';
import { Loading, Error } from '../components';
import { reducePhotos } from '../utils';
import '@rmwc/grid/styles';

const GET_MEDIA_ITEMS = gql`
  query getMediaItems {
    mediaItems {
      nodes {
        id
        imageUrl
        mimeType
        fileName
        createdAt
        updatedAt
        mediaMetadata {
          creationTime
        }
      }
    }
  }
`;

const Photos = () => {
  const { loading, error, data } = useQuery(GET_MEDIA_ITEMS, {
    fetchPolicy: 'no-cache',
  });

  if (loading) return <Loading />;
  if (error) return <Error />;

  return (
    <>
      {data && data.mediaItems && (
        <>
          {data.mediaItems.nodes.length === 0 ? (
            <>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <img src="/images.svg" width="100%" />
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <center>Upload your photos to iris!</center>
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
            </>
          ) : (
            <>
              {reducePhotos(data.mediaItems.nodes).map((image) => {
                return (
                  <div key={image.createdAt}>
                    <Grid>
                      <GridCell desktop={10} tablet={6} phone={3}>
                        {moment(image.createdAt).format('MMMM D, YYYY')}
                      </GridCell>
                    </Grid>
                    <Grid>
                      {image.imageUrl.map((img, index) => {
                        return (
                          <GridCell
                            key={image.id[index]}
                            desktop={2}
                            tablet={4}
                            phone={12}
                          >
                            <Link to={`photo/${image.id[index]}`}>
                              <img
                                key={image.id[index]}
                                src={`${img}?width=200&height=200`}
                                width="100%"
                                style={{
                                  cursor: 'pointer',
                                  borderRadius: '4px',
                                  height: '180px',
                                  objectFit: 'cover',
                                }}
                              />
                            </Link>
                          </GridCell>
                        );
                      })}
                    </Grid>
                  </div>
                );
              })}
            </>
          )}
        </>
      )}
    </>
  );
};

export default Photos;
