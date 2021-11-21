import React, { useState } from 'react';
import moment from 'moment';
import { useHistory } from 'react-router-dom';
import { useParams } from 'react-router-dom';
import { gql, useQuery } from '@apollo/client';
import { Icon } from '@rmwc/icon';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import { Grid, GridCell } from '@rmwc/grid';
import '@rmwc/grid/styles';
import { Loading, Error, DeleteAlbumDialog, EditAlbum } from '../components';

const GET_ALBUM = gql`
  query getAlbum($id: String!) {
    album(id: $id) {
      id
      name
      description
      createdAt
      mediaItems {
        totalCount
        nodes {
          id
          imageUrl
        }
      }
    }
  }
`;

const Album = () => {
  let history = useHistory();
  let { id } = useParams();
  const { error, loading, data } = useQuery(GET_ALBUM, {
    variables: { id },
    fetchPolicy: 'no-cache',
  });

  if (error) return <Error />;

  const styleFav = {
    radius: '4px',
    width: '180px',
    margin: '0px 6px 8px 6px',
  };

  const [open, setOpen] = useState(false);

  return (
    <>
      {loading ? (
        <Loading />
      ) : (
        <>
          <Grid>
            <GridCell span={12}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'start',
                  alignItems: 'center',
                }}
              >
                <EditAlbum
                  albumName={data.album.name}
                  albumId={data.album.id}
                />
                &nbsp;&nbsp;&nbsp;
                <Icon
                  onClick={() => setOpen(true)}
                  style={{ cursor: 'pointer', color: '#424242' }}
                  icon={{ icon: 'delete', size: 'small' }}
                />
                <DeleteAlbumDialog
                  open={open}
                  setOpen={setOpen}
                  albumName={data.album.name}
                  albumId={data.album.id}
                />
              </div>
              <span style={{ color: '#424242' }}>
                {moment(data.album.createdAt).format('MMMM D, YYYY')}
              </span>
            </GridCell>
          </Grid>
          <Grid>
            <GridCell desktop={12} tablet={12} phone={12}>
              <ImageList>
                {data.album.mediaItems.nodes.map((img) => (
                  <ImageListItem key={img.id} style={styleFav}>
                    <ImageListImageAspectContainer>
                      <ImageListImage
                        src={`${img.imageUrl}?width=200&height=200`}
                        style={{ cursor: 'pointer', borderRadius: '4px' }}
                        onClick={() => history.push(`/photo/${img.id}`)}
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
  );
};

export default Album;
