import React from 'react';
import { useParams } from 'react-router-dom';
import { useHistory } from 'react-router-dom';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import { Grid, GridCell } from '@rmwc/grid';
import { Loading, Error } from '../../components';
import { gql, useQuery } from '@apollo/client';
import { capThings } from '../../utils';
import '@rmwc/list/styles';

const GET_MEDIA_ITEM = gql`
  query getMediaItem($id: String!) {
    entity(id: $id) {
      name
      mediaItems {
        nodes {
          id
          imageUrl
          entities {
            name
          }
        }
      }
    }
  }
`;

const Entity = () => {
  let { id } = useParams();
  const { error, data } = useQuery(GET_MEDIA_ITEM, {
    variables: { id },
  });

  if (error) return <Error />;

  let history = useHistory();
  const stylePlacesThigsList = {
    radius: '4px',
    width: '180px',
    margin: '6px 6px 6px 6px',
  };

  return (
    <>
      {data && data.entity?.mediaItems?.nodes ? (
        <>
          <Grid>
            <GridCell desktop="10" tablet="6" phone="3">
              {capThings(data.entity?.name)}
            </GridCell>
          </Grid>
          <Grid>
            <GridCell desktop={12} tablet={12} phone={12}>
              <ImageList withTextProtection>
                {data.entity?.mediaItems?.nodes.map((src) => (
                  <ImageListItem key={src.id} style={stylePlacesThigsList}>
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
      ) : (
        <Loading />
      )}
    </>
  );
};

export default Entity;
