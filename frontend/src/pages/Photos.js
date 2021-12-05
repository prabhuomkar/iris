import React, { useState, useContext } from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import { Link } from 'react-router-dom';
import { gql, useQuery } from '@apollo/client';
import { Grid, GridCell } from '@rmwc/grid';
import { Icon } from '@rmwc/icon';
import '@rmwc/grid/styles';
import { Loading, Error } from '../components';
import { reducePhotos, sortPhotos } from '../utils';
import { CreateAlbumContext } from '../App';

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

const Photo = ({ imageId, imageUrl, imageList, setImageList }) => {
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
      <Link to={`photo/${imageId}`}>
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

  const { imageList, setImageList } = useContext(CreateAlbumContext);

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
                              imageList={imageList}
                              setImageList={setImageList}
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
};

export default Photos;
