import React from 'react';
import moment from 'moment';
import { gql, useQuery } from '@apollo/client';
import { Grid, GridCell } from '@rmwc/grid';
import { reducePhotos } from '../utils';
import '@rmwc/grid/styles';

const GET_MEDIA = gql`
  query GetMedia {
    mediaItems {
      nodes {
        id
        imageUrl
        mimeType
        fileName
        createdAt
        updatedAt
      }
    }
  }
`;

const Photos = () => {
  const { loading, error, data } = useQuery(GET_MEDIA);

  if (loading) return 'Loading...';
  if (error) return `Error! ${error.message}`;

  return (
    <>
      {data && data.mediaItems && (
        <>
          {reducePhotos(data.mediaItems.nodes).map((image) => {
            return (
              <>
                <Grid>
                  <GridCell desktop={10} tablet={6} phone={3}>
                    {moment(image.createdAt).format('MMMM D, YYYY')}
                  </GridCell>
                </Grid>
                <Grid>
                  {image.imageUrl.map((img, index) => {
                    const imageId = image.id[index];
                    return (
                      <GridCell
                        key={image.id[index]}
                        desktop={2}
                        tablet={4}
                        phone={12}
                      >
                        <img
                          key={image.id[index]}
                          src={img}
                          width="100%"
                          onClick={() => console.log(imageId)}
                        />
                      </GridCell>
                    );
                  })}
                </Grid>
              </>
            );
          })}
        </>
      )}
    </>
  );
};

export default Photos;
