import React, { useState } from 'react';
import moment from 'moment';
import { Fraction } from 'fractional';
import { useParams } from 'react-router-dom';
import { gql, useQuery, useMutation } from '@apollo/client';
import { Grid, GridCell } from '@rmwc/grid';
import { Button } from '@rmwc/button';
import { TextField } from '@rmwc/textfield';
import { CircularProgress } from '@rmwc/circular-progress';
import {
  List,
  ListItem,
  ListItemGraphic,
  ListItemPrimaryText,
  ListItemSecondaryText,
  ListItemText,
} from '@rmwc/list';
import '@rmwc/list/styles';
import { capThings } from '../utils';
import { Loading, Error, FaceList, FavouriteAction } from '../components';
const prettyBytes = require('pretty-bytes');

const GET_MEDIA_ITEM = gql`
  query getMediaItem($id: String!) {
    mediaItem(id: $id) {
      id
      description
      imageUrl
      mimeType
      fileName
      fileSize
      contentCategories
      favourite
      entities {
        entityType
        name
        imageUrl
        id
      }
      mediaMetadata {
        creationTime
        width
        height
        photo {
          cameraMake
          cameraModel
          focalLength
          apertureFNumber
          isoEquivalent
          exposureTime
        }
        creationTime
        location {
          latitude
          longitude
        }
      }
      createdAt
      updatedAt
    }
  }
`;

const UPDATE_DESCRIPTION = gql`
  mutation updateDescription($id: String!, $description: String!) {
    updateDescription(id: $id, description: $description)
  }
`;

const Photo = () => {
  let { id } = useParams();
  const { error, data } = useQuery(GET_MEDIA_ITEM, {
    variables: { id },
    fetchPolicy: 'no-cache',
  });

  const [
    updateDescription,
    { loading: updateDescriptionLoading, error: updateDescriptionError },
  ] = useMutation(UPDATE_DESCRIPTION);

  if (error) return <Error />;

  const entityTypeIcon = (type) => {
    let typeIcon = '';
    switch (type) {
      case 'things':
        typeIcon = 'visibility';
        break;
      case 'places':
        typeIcon = 'location_on';
        break;
      case 'people':
        typeIcon = 'people';
        break;
      default:
        typeIcon = 'visibility';
    }
    return typeIcon;
  };

  const getEntity = (data, eType) =>
    data
      .filter((e) => e.entityType === eType)
      .reduce((prev, curr) => {
        prev.push(curr.name);
        return prev;
      }, []);

  const things = getEntity(data?.mediaItem?.entities ?? [], 'things');
  const places = getEntity(data?.mediaItem?.entities ?? [], 'places');
  const people = getEntity(data?.mediaItem?.entities ?? [], 'people');

  const handleEditDescription = (entityId, updatedDescriptionName) => {
    updateDescription({
      variables: { id: entityId, description: updatedDescriptionName },
    });
    setEditDescription(updatedDescriptionName);
  };

  const [editDescription, setEditDescription] = useState(
    data?.mediaItem?.description
  );

  return (
    <>
      {data && data.mediaItem ? (
        <Grid>
          <GridCell
            desktop={6}
            tablet={6}
            phone={12}
            className="photo-grid-cell"
          >
            <div>
              <img src={data.mediaItem.imageUrl} width="100%" />
            </div>
            <div className="fav-icon">
              <FavouriteAction
                liked={data.mediaItem.favourite}
                id={data.mediaItem.id}
              />
            </div>
          </GridCell>
          <GridCell desktop={6} tablet={4} phone={12}>
            <>
              <ListItem style={{ height: '60px' }}>
                <ListItemGraphic icon="description" />
                <ListItemText>
                  <TextField
                    placeholder="Add description"
                    defaultValue={
                      editDescription
                        ? editDescription
                        : data.mediaItem?.description
                    }
                    onChange={(e) => setEditDescription(e.target.value)}
                    style={{ height: '36px' }}
                  />
                  &nbsp;&nbsp;
                  <Button
                    label="update"
                    disabled={editDescription ? false : true}
                    onClick={() =>
                      handleEditDescription(data.mediaItem?.id, editDescription)
                    }
                    unelevated
                    style={{ color: '#fff' }}
                  />
                  &nbsp;&nbsp;&nbsp;
                  {updateDescriptionLoading && (
                    <CircularProgress size="medium" />
                  )}
                  {updateDescriptionError && (
                    <>Sorry, some error occured while updating name</>
                  )}
                </ListItemText>
              </ListItem>
            </>
            {data.mediaItem && data.mediaItem?.contentCategories && (
              <ListItem>
                <ListItemGraphic icon="category" />
                <ListItemText>
                  {data.mediaItem?.contentCategories.join(', ')}
                </ListItemText>
              </ListItem>
            )}
            {data.mediaItem?.entities && (
              <>
                <List>
                  {people && people.length > 0 && (
                    <>
                      <div style={{ marginLeft: '60px' }}>
                        <FaceList
                          type="people"
                          data={data.mediaItem?.entities}
                        />
                      </div>
                    </>
                  )}
                  {things && things.length > 0 && (
                    <ListItem>
                      <ListItemGraphic icon={entityTypeIcon('things')} />
                      <ListItemText>
                        {capThings(things.join(', '))}
                      </ListItemText>
                    </ListItem>
                  )}
                  {places && places.length > 0 && (
                    <ListItem>
                      <ListItemGraphic icon={entityTypeIcon('places')} />
                      <ListItemText>{places.join(', ')}</ListItemText>
                    </ListItem>
                  )}
                </List>
              </>
            )}

            <List twoLine>
              <ListItem>
                <ListItemGraphic icon="today" />
                <ListItemText>
                  <ListItemPrimaryText>
                    {moment(
                      data.mediaItem?.mediaMetadata?.creationTime ||
                        data.mediaItem.createdAt
                    ).format('MMMM D, YYYY')}
                  </ListItemPrimaryText>
                  <ListItemSecondaryText>
                    {moment(
                      data.mediaItem?.mediaMetadata?.creationTime ||
                        data.mediaItem.createdAt
                    ).format('dddd')}
                    ,{' '}
                    {moment(
                      data.mediaItem?.mediaMetadata?.creationTime ||
                        data.mediaItem.createdAt
                    ).format('h:mm a')}
                  </ListItemSecondaryText>
                </ListItemText>
              </ListItem>
              <ListItem>
                <ListItemGraphic icon="image" />
                <ListItemText>
                  <ListItemPrimaryText>
                    {data.mediaItem.fileName}
                  </ListItemPrimaryText>
                  <ListItemSecondaryText>
                    {data.mediaItem.mediaMetadata?.width &&
                      data.mediaItem.mediaMetadata?.height && (
                        <>
                          {data.mediaItem.mediaMetadata?.width}x
                          {data.mediaItem.mediaMetadata?.height}{' '}
                        </>
                      )}
                    {prettyBytes(data.mediaItem.fileSize)}
                  </ListItemSecondaryText>
                </ListItemText>
              </ListItem>
              {data.mediaItem.mediaMetadata?.photo?.cameraMake &&
                data.mediaItem.mediaMetadata?.photo?.cameraModel &&
                data.mediaItem.mediaMetadata?.photo?.focalLength &&
                data.mediaItem.mediaMetadata?.photo?.apertureFNumber &&
                data.mediaItem.mediaMetadata?.photo?.focalLength &&
                data.mediaItem.mediaMetadata?.photo?.isoEquivalent && (
                  <>
                    <ListItem>
                      <ListItemGraphic icon="camera" />
                      <ListItemText>
                        <ListItemPrimaryText>
                          {data.mediaItem.mediaMetadata?.photo?.cameraMake}{' '}
                          {data.mediaItem.mediaMetadata?.photo?.cameraModel}
                        </ListItemPrimaryText>
                        <ListItemSecondaryText>
                          f/
                          {
                            data.mediaItem.mediaMetadata?.photo?.apertureFNumber
                          }{' '}
                          {new Fraction(
                            data.mediaItem.mediaMetadata?.photo?.exposureTime?.toFixed(
                              2
                            )
                          ).toString()}{' '}
                          {data.mediaItem.mediaMetadata?.photo?.focalLength}
                          mm ISO{''}
                          {data.mediaItem.mediaMetadata?.photo?.isoEquivalent}
                        </ListItemSecondaryText>
                      </ListItemText>
                    </ListItem>
                  </>
                )}
            </List>
          </GridCell>
        </Grid>
      ) : (
        <>
          <Loading />
        </>
      )}
    </>
  );
};

export default Photo;
