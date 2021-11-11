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
import { capThings } from '../../utils';

const ExplorePeopleList = ({ data, type }) => {
  let history = useHistory();
  const stylePeopleList = {
    radius: '50%',
    width: '126px',
    margin: '0px 6px 8px 6px',
  };

  return (
    <>
      <ImageList>
        {data.map((src) => (
          <ImageListItem key={src.id} style={stylePeopleList}>
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
              <ImageListLabel
                style={{
                  justifyContent: 'center',
                  display: 'flex',
                }}
              >
                {capThings(src.name)}
              </ImageListLabel>
            </ImageListSupporting>
          </ImageListItem>
        ))}
      </ImageList>
    </>
  );
};

ExplorePeopleList.propTypes = {
  type: PropTypes.string,
  data: PropTypes.array,
};

export default ExplorePeopleList;
