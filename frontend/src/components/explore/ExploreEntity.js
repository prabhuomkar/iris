import React from 'react';
import PropTypes from 'prop-types';
import { useHistory } from 'react-router-dom';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListSupporting,
  ImageListLabel,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import { capThings } from '../../utils';
import '@rmwc/image-list/styles';

const ExploreEntity = ({ type, data }) => {
  let history = useHistory();
  const stylePlacesThigsList = {
    radius: '4px',
    width: '180px',
    margin: '0px 6px 8px 6px',
  };
  return (
    <>
      <ImageList withTextProtection>
        {data.map((src) => (
          <ImageListItem key={src.id} style={stylePlacesThigsList}>
            <ImageListImageAspectContainer>
              <ImageListImage
                src={`${src.imageUrl}?width=200&height=200`}
                style={{ cursor: 'pointer', borderRadius: '4px' }}
                onClick={() => history.push(`/explore/${type}/${src.id}`)}
              />
            </ImageListImageAspectContainer>
            <ImageListSupporting>
              <ImageListLabel>{capThings(src.name)}</ImageListLabel>
            </ImageListSupporting>
          </ImageListItem>
        ))}
      </ImageList>
    </>
  );
};

ExploreEntity.propTypes = {
  data: PropTypes.array,
  type: PropTypes.string,
};

export default ExploreEntity;
