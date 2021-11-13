import React from 'react';
import { useHistory } from 'react-router-dom';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListSupporting,
  ImageListLabel,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import { capEntityName } from '../utils';

const PeopleList = (data) => {
  let history = useHistory();
  const stylePeopleList = {
    width: '80px',
    margin: '8px 6px 8px 6px',
  };

  const getEntity = (data) =>
    data
      .filter((e) => e.entityType === 'people')
      .reduce((prev, curr) => {
        prev.push(curr);
        return prev;
      }, []);

  return (
    <>
      <ImageList>
        {getEntity(data.data).map((src) => (
          <ImageListItem key={src.id} style={stylePeopleList}>
            <ImageListImageAspectContainer>
              <ImageListImage
                src={`${src.imageUrl}?width=150&height=150`}
                onClick={() =>
                  history.push(`/explore/${src.entityType}/${src.id}`)
                }
                style={{ borderRadius: '6px', cursor: 'pointer' }}
              />
            </ImageListImageAspectContainer>
            <ImageListSupporting>
              <ImageListLabel
                style={{
                  justifyContent: 'center',
                  display: 'flex',
                }}
              >
                {capEntityName(src.name)}
              </ImageListLabel>
            </ImageListSupporting>
          </ImageListItem>
        ))}
      </ImageList>
    </>
  );
};

export default PeopleList;
