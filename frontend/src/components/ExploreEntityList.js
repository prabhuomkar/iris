import React from 'react';
import PropTypes from 'prop-types';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import '@rmwc/image-list/styles';

const ExploreEntityList = ({ listRadius, listWidth, listMargin, data }) => {
  return (
    <>
      <ImageList>
        {data.map((src) => (
          <ImageListItem
            key={src}
            style={{ width: listWidth, margin: listMargin }}
          >
            <ImageListImageAspectContainer>
              <ImageListImage
                src={src}
                style={{ borderRadius: listRadius, cursor: 'pointer' }}
              />
            </ImageListImageAspectContainer>
          </ImageListItem>
        ))}
      </ImageList>
    </>
  );
};

ExploreEntityList.propTypes = {
  listRadius: PropTypes.string,
  listWidth: PropTypes.string,
  listMargin: PropTypes.string,
  data: PropTypes.array,
};

export default ExploreEntityList;
