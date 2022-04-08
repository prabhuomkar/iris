import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useHistory } from 'react-router-dom';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import { Grid, GridCell } from '@rmwc/grid';
import { Button } from '@rmwc/button';
import { TextField } from '@rmwc/textfield';
import { Loading, Error } from '../../components';
import { CircularProgress } from '@rmwc/circular-progress';
import { gql, useQuery, useMutation } from '@apollo/client';
import { capEntityName } from '../../utils';
import '@rmwc/list/styles';
import '@rmwc/textfield/styles';
import '@rmwc/circular-progress/styles';

const GET_MEDIA_ITEM = gql`
  query getMediaItem($id: String!) {
    entity(id: $id) {
      name
      id
      entityType
      mediaItems {
        nodes {
          id
          previewUrl
          entities {
            name
          }
        }
      }
    }
  }
`;

const UPDATE_ENTITY = gql`
  mutation updateEntity($id: String!, $name: String!) {
    updateEntity(id: $id, name: $name)
  }
`;

const Entity = () => {
  let { id } = useParams();

  const { error, data } = useQuery(GET_MEDIA_ITEM, {
    variables: { id },
    fetchPolicy: 'no-cache',
  });

  const [
    updateEntity,
    { loading: updateEntityLoading, error: updateEntityError },
  ] = useMutation(UPDATE_ENTITY);

  const [showEdit, setShowEdit] = useState(false);

  if (error) return <Error />;

  let history = useHistory();
  const stylePlacesThigsList = {
    radius: '4px',
    width: '180px',
    margin: '6px 6px 6px 6px',
  };

  const handleEditEntity = (entityId, updatedEntityName) => {
    updateEntity({ variables: { id: entityId, name: updatedEntityName } });
    setShowEdit(false);
  };

  const [editEntity, setEditEntity] = useState(data?.entity?.name);

  return (
    <>
      {data && data.entity?.mediaItems?.nodes ? (
        <>
          <Grid>
            <GridCell desktop="10" tablet="6" phone="3">
              {showEdit ? (
                <>
                  {data.entity?.entityType === 'people' && (
                    <div className="edit-section">
                      <TextField
                        defaultValue={
                          editEntity
                            ? editEntity
                            : capEntityName(data.entity?.name)
                        }
                        onChange={(e) => setEditEntity(e.target.value)}
                        style={{ height: '36px' }}
                      />
                      &nbsp;&nbsp;&nbsp;
                      <Button
                        onClick={() =>
                          handleEditEntity(data.entity?.id, editEntity)
                        }
                        label="update"
                        unelevated
                        disabled={editEntity ? false : true}
                        style={{ color: '#fff' }}
                      />
                      &nbsp;&nbsp;&nbsp;
                      <Button
                        onClick={() => setShowEdit(!showEdit)}
                        label="cancel"
                        outlined
                      />
                      &nbsp;&nbsp;&nbsp;
                      {updateEntityLoading && (
                        <CircularProgress size="medium" />
                      )}
                      {updateEntityError && (
                        <>Sorry, some error occured while updating name</>
                      )}
                    </div>
                  )}
                </>
              ) : (
                <>
                  {data.entity?.entityType === 'people' ? (
                    <>
                      {editEntity
                        ? editEntity
                        : capEntityName(data.entity.name)}
                      &nbsp;&nbsp;&nbsp;
                      <Button
                        icon="edit"
                        label="Edit"
                        onClick={() => setShowEdit(!showEdit)}
                        outlined
                      />
                    </>
                  ) : (
                    <>{capEntityName(data.entity?.name)}</>
                  )}
                </>
              )}
            </GridCell>
          </Grid>
          <Grid>
            <GridCell desktop={12} tablet={12} phone={12}>
              <ImageList withTextProtection>
                {data.entity?.mediaItems?.nodes.map((src) => (
                  <ImageListItem key={src.id} style={stylePlacesThigsList}>
                    <ImageListImageAspectContainer>
                      <ImageListImage
                        src={`${src.previewUrl}?width=200&height=200`}
                        style={{ cursor: 'pointer', borderRadius: '4px' }}
                        onClick={() => history.push(`/photo/${src.id}`)}
                      />
                    </ImageListImageAspectContainer>
                  </ImageListItem>
                ))}
              </ImageList>
            </GridCell>
          </Grid>
        </>
      ) : (
        <Loading />
      )}
    </>
  );
};

export default Entity;
