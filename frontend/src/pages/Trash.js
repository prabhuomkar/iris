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

const GET_DELETED = gql`
  query getDeleted {
    deleted {
      totalCount
      nodes {
        id
        previewUrl
      }
    }
  }
`;

const Trash = () => {
  const { error: delError, data: delData } = useQuery(GET_DELETED, {
    fetchPolicy: 'no-cache',
  });
  if (delError) return <Error />;

  let history = useHistory();
  const styleFav = {
    radius: '4px',
    width: '180px',
    margin: '0px 6px 8px 6px',
  };

  return (
    <>
      {delData && delData.deleted && delData.deleted.nodes ? (
        <>
          {delData.deleted && delData.deleted.totalCount === 0 ? (
            <>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <center>
                    <img src="/favourites.svg" width="100%" />
                    <br />
                    <br />
                    Nothing in trash!
                  </center>
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
            </>
          ) : (
            <>
              <Grid className="grid-cols">
                <GridCell desktop={10} tablet={6} phone={3}>
                  Trash
                </GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={12} tablet={12} phone={12}>
                  <ImageList>
                    {delData.deleted.nodes.map((src) => (
                      <ImageListItem key={src.id} style={styleFav}>
                        <ImageListImageAspectContainer>
                          <ImageListImage
                            src={`${src.previewUrl}?width=200&height=200`}
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

export default Trash;
