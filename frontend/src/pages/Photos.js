import React from 'react';
import moment from 'moment';
import { reducePhotos } from '../utils';
import { gql, useQuery } from '@apollo/client';
import { Grid, GridCell } from '@rmwc/grid';
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
  console.log(data.mediaItems.nodes);
  console.log(reducePhotos(data.mediaItems.nodes));

  return (
    <>
      {data && data.mediaItems && (
        <>
          {/*
          {data.mediaItems.nodes.map((img) => {
            return (
              <GridCell desktop={2} tablet={4} phone={12} key={img}>
                <img src={img.imageUrl} width="100%" />
              </GridCell>
            );
          })}
          */}
          {reducePhotos(data.mediaItems.nodes).map((image) => {
            return (
              <>
                <Grid>
                  <GridCell desktop={10} tablet={6} phone={3}>
                    {moment(image.createdAt).format('MMMM D, YYYY')}
                  </GridCell>
                </Grid>
                <Grid>
                  {image.imageUrl.map((img) => {
                    return (
                      <GridCell desktop={2} tablet={4} phone={12} key={img}>
                        <img key={img} src={img} width="100%" />
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
