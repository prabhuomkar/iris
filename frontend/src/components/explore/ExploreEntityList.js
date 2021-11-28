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
import { capEntityName } from '../../utils';

const ExploreEntityList = ({ data, type }) => {
  let history = useHistory();
  const stylePeople = {
    radius: '50%',
    width: '126px',
    margin: '0px 6px 8px 6px',
  };

  const stylePlacesThigs = {
    radius: '4px',
    width: '180px',
    margin: '0px 6px 8px 6px',
  };

  return (
    <>
      <ImageList withTextProtection={type === 'people' ? false : true}>
        {data.map((src) => (
          <ImageListItem
            key={src.id}
            style={type === 'people' ? stylePeople : stylePlacesThigs}
          >
            <ImageListImageAspectContainer>
              <ImageListImage
                src={`${src?.displayMediaItem?.imageUrl}?width=200&height=200`}
                onClick={() => history.push(`/explore/${type}/${src.id}`)}
                style={{
                  borderRadius:
                    type === 'people'
                      ? stylePeople.radius
                      : stylePlacesThigs.radius,
                  cursor: 'pointer',
                }}
              />
            </ImageListImageAspectContainer>
            <ImageListSupporting>
              {type === 'people' ? (
                <ImageListLabel
                  style={{
                    justifyContent: 'center',
                    display: 'flex',
                  }}
                >
                  {capEntityName(src.name)}
                </ImageListLabel>
              ) : (
                <ImageListLabel>{capEntityName(src.name)}</ImageListLabel>
              )}
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
