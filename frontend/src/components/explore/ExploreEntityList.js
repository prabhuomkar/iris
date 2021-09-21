import React from 'react';
import PropTypes from 'prop-types';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import '@rmwc/image-list/styles';

const ExploreEntityList = ({ data, type }) => {
  const stylePeopleList = {
    radius: '50%',
    width: '10%',
    margin: '0px 6px 6px 6px',
  };

  const stylePlacesThigsList = {
    radius: '6px',
    width: '13%',
    margin: '0px 6px 12px 6px',
  };

  return (
    <>
      <ImageList>
        {data.map((src) => (
          <ImageListItem
            key={src}
            style={
              type === 'PeopleList' ? stylePeopleList : stylePlacesThigsList
            }
          >
            <ImageListImageAspectContainer>
              <ImageListImage
                src={src}
                style={{
                  borderRadius:
                    type === 'PeopleList'
                      ? stylePeopleList.radius
                      : stylePlacesThigsList.radius,
                  cursor: 'pointer',
                }}
              />
            </ImageListImageAspectContainer>
          </ImageListItem>
        ))}
      </ImageList>
    </>
  );
};

ExploreEntityList.propTypes = {
  type: PropTypes.string,
  data: PropTypes.array,
};

export default ExploreEntityList;
