import React, { useState, useContext } from 'react';
import PropTypes from 'prop-types';
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
import { Button } from '@rmwc/button';
import { Grid, GridCell } from '@rmwc/grid';
import '@rmwc/grid/styles';
import { Loading, Error, DeleteAlbumDialog, EditAlbum } from '../components';
import { RemoveAlbumPhotosContext } from '../App';

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

const AlbumPhoto = ({
  imageUrl,
  imageId,
  removeImageList,
  setRemoveImageList,
}) => {
  let history = useHistory();

  const [isSelected, setIsSelected] = useState(false);

  const onSelect = () => {
    if (removeImageList.includes(imageId)) {
      setRemoveImageList((arr) =>
        arr.filter((_imageId) => _imageId !== imageId)
      );
      setIsSelected(!isSelected);
    } else {
      setRemoveImageList((arr) => [...arr, imageId]);
      setIsSelected(!isSelected);
    }
  };
  return (
    <div className="select-photo">
      <Icon
        icon={{
          icon: 'check_circle',
          size: 'medium',
        }}
        className="select-icon"
        style={{
          color: isSelected ? '#4800b2' : '#ffffff',
          cursor: 'pointer',
          zIndex: '1',
        }}
        onClick={onSelect}
      />
      <ImageListImageAspectContainer>
        <ImageListImage
          src={`${imageUrl}?width=200&height=200`}
          style={{ cursor: 'pointer', borderRadius: '4px' }}
          onClick={() => history.push(`/photo/${imageId}`)}
        />
      </ImageListImageAspectContainer>
    </div>
  );
};

const Album = () => {
  let { id } = useParams();
  const { error, loading, data } = useQuery(GET_ALBUM, {
    variables: { id },
    fetchPolicy: 'no-cache',
  });

  const { removeImageList, setRemoveImageList } = useContext(
    RemoveAlbumPhotosContext
  );

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
          {data?.album?.mediaItems?.totalCount !== 0 ? (
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
                    &nbsp;&nbsp;&nbsp;
                    <Button icon="add" label="Add photos" outlined />
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
                        <AlbumPhoto
                          imageUrl={img.imageUrl}
                          imageId={img.id}
                          removeImageList={removeImageList}
                          setRemoveImageList={setRemoveImageList}
                        />
                      </ImageListItem>
                    ))}
                  </ImageList>
                </GridCell>
              </Grid>
            </>
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
                    &nbsp;&nbsp;&nbsp;
                    <Button icon="add" label="Add photos" outlined />
                  </div>
                </GridCell>
              </Grid>
            </>
          )}
        </>
      )}
    </>
  );
};

AlbumPhoto.propTypes = {
  imageUrl: PropTypes.string,
  imageId: PropTypes.string,
  removeImageList: PropTypes.array,
  setRemoveImageList: PropTypes.func,
};

export default Album;
