import React, { useState, useContext } from 'react';
import { useRouteMatch, useParams } from 'react-router-dom';
import PropTypes from 'prop-types';
import moment from 'moment';
import { Link } from 'react-router-dom';
import { gql, useQuery } from '@apollo/client';
import { Grid, GridCell } from '@rmwc/grid';
import { Icon } from '@rmwc/icon';
import '@rmwc/grid/styles';
import { Loading, Error, UpdateAlbum } from '../components';
import { reducePhotos, sortPhotos } from '../utils';
import { AlbumsContext } from '../App';

const GET_MEDIA_ITEMS = gql`
  query getMediaItems {
    mediaItems(page: 1, limit: 100) {
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

const Photo = ({ imageId, imageUrl, imageList, setImageList, match }) => {
  const [isSelected, setIsSelected] = useState(false);

  const onSelect = () => {
    if (imageList.includes(imageId)) {
      setImageList((arr) => arr.filter((_imageId) => _imageId !== imageId));
      setIsSelected(!isSelected);
    } else {
      setImageList((arr) => [...arr, imageId]);
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
        }}
        onClick={onSelect}
      />

      <Link to={match ? '#' : `photo/${imageId}`}>
        <img
          key={imageId}
          src={`${imageUrl}?width=200&height=200`}
          width="100%"
          style={{
            cursor: 'pointer',
            borderRadius: '4px',
            height: '180px',
            objectFit: 'cover',
          }}
        />
      </Link>
    </div>
  );
};

const Photos = () => {
  const { loading, error, data } = useQuery(GET_MEDIA_ITEMS, {
    fetchPolicy: 'no-cache',
  });
  const params = useParams();
  let match = useRouteMatch('/album/:id/add');

  const { createAlbum, addPhotos } = useContext(AlbumsContext);

  const [imageList, setImageList] = createAlbum;
  const [addImageList, setAddImageList] = addPhotos;

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
                  <center>
                    <img src="/images.svg" width="100%" />
                    <br />
                    <br />
                    Upload your photos to iris!
                  </center>
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
            </>
          ) : (
            <>
              {match?.isExact && (
                <Grid>
                  <GridCell desktop={10} tablet={6} phone={3}>
                    <h3
                      style={{ display: 'inline-block', marginRight: '16px' }}
                    >
                      Select Photos
                    </h3>
                    <UpdateAlbum
                      addImageList={addImageList}
                      disabled={addImageList.length === 0}
                      albumId={params.id}
                    />
                  </GridCell>
                </Grid>
              )}
              {sortPhotos(reducePhotos(data.mediaItems.nodes)).map((image) => {
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
                            <Photo
                              imageId={image.id[index]}
                              imageUrl={img}
                              imageList={
                                match?.isExact ? addImageList : imageList
                              }
                              setImageList={
                                match?.isExact ? setAddImageList : setImageList
                              }
                              match={match?.isExact}
                            />
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

Photo.propTypes = {
  imageId: PropTypes.string,
  imageUrl: PropTypes.string,
  imageList: PropTypes.array,
  setImageList: PropTypes.func,
  match: PropTypes.bool,
};

export default Photos;
