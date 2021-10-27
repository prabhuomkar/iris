import React from 'react';
import PropTypes from 'prop-types';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListSupporting,
  ImageListLabel,
} from '@rmwc/image-list';
import '@rmwc/image-list/styles';

const ExploreEntity = ({ data }) => {
  return (
    <>
      <ImageList
        withTextProtection
        style={{
          columnGap: '12px',
        }}
      >
        {data.map((src) => (
          <ImageListItem key={src.imageUrl} style={{ marginBottom: '12px' }}>
            <ImageListImage src={src.imageUrl} style={{ width: '180px' }} />
            <ImageListSupporting>
              <ImageListLabel>{src.name}</ImageListLabel>
            </ImageListSupporting>
          </ImageListItem>
        ))}
      </ImageList>
    </>
  );
};

ExploreEntity.propTypes = {
  data: PropTypes.array,
};

export default ExploreEntity;
