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
import '@rmwc/image-list/styles';

const ExploreEntityList = ({ data, type }) => {
  let history = useHistory();
  const stylePeopleList = {
    radius: '50%',
    width: '10%',
    margin: '0px 6px 6px 6px',
  };

  const stylePlacesThigsList = {
    radius: '4px',
    width: '180px',
    margin: '0px 6px 12px 6px',
  };

  return (
    <>
      <ImageList withTextProtection>
        {data.map((src) => (
          <ImageListItem
            key={src.id}
            style={type === 'people' ? stylePeopleList : stylePlacesThigsList}
          >
            <ImageListImageAspectContainer>
              <ImageListImage
                src={`${src.imageUrl}?width=200&height=200`}
                onClick={() => history.push(`/explore/${type}/${src.id}`)}
                style={{
                  borderRadius:
                    type === 'people'
                      ? stylePeopleList.radius
                      : stylePlacesThigsList.radius,
                  cursor: 'pointer',
                }}
              />
            </ImageListImageAspectContainer>
            <ImageListSupporting>
              <ImageListLabel>{src.name}</ImageListLabel>
            </ImageListSupporting>
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
