import React from 'react';
import moment from 'moment';
import { Fraction } from 'fractional';
import { useParams } from 'react-router-dom';
import { Grid, GridCell } from '@rmwc/grid';
import {
  List,
  ListItem,
  ListItemGraphic,
  ListItemPrimaryText,
  ListItemSecondaryText,
  ListItemText,
} from '@rmwc/list';
import { capThings } from '../utils';
import { Loading, Error } from '../components';
import { gql, useQuery } from '@apollo/client';
import '@rmwc/list/styles';
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
      entities {
        entityType
        name
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

const Photo = () => {
  let { id } = useParams();
  const { error, data } = useQuery(GET_MEDIA_ITEM, {
    variables: { id },
    fetchPolicy: 'no-cache',
  });

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

  return (
    <>
      {data && data.mediaItem ? (
        <Grid>
          <GridCell desktop={6} tablet={6} phone={12}>
            <img src={data.mediaItem.imageUrl} width="100%" />
          </GridCell>
          <GridCell desktop={4} tablet={4} phone={12}>
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
            {data.mediaItem?.entities && (
              <>
                <List>
                  {things && things.length > 0 && (
                    <ListItem>
                      <ListItemGraphic icon={entityTypeIcon('things')} />
                      <ListItemText>
                        {capThings(things.join(', '))}
                      </ListItemText>
                    </ListItem>
                  )}
                  {people && people.length > 0 && (
                    <ListItem>
                      <ListItemGraphic icon={entityTypeIcon('people')} />
                      <ListItemText>
                        {capThings(people.join(', '))}
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
