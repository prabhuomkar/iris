import React from 'react';
import PropTypes from 'prop-types';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import '@rmwc/image-list/styles';

const ExploreImageList = ({ listRadius, data }) => {
  return (
    <>
      <ImageList>
        {data.map((src) => (
          <ImageListItem key={src} style={{ width: '10%', margin: '0px 6px' }}>
            <ImageListImageAspectContainer>
              <ImageListImage src={src} style={{ borderRadius: listRadius }} />
            </ImageListImageAspectContainer>
          </ImageListItem>
        ))}
      </ImageList>
    </>
  );
};

ExploreImageList.propTypes = {
  listRadius: PropTypes.string,
  data: PropTypes.array,
};

export default ExploreImageList;
