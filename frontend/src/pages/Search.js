import React from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import { useQuery, gql } from '@apollo/client';
import { Loading, Error } from '../components';
import { Grid, GridCell } from '@rmwc/grid';
import {
  ImageList,
  ImageListImage,
  ImageListItem,
  ImageListImageAspectContainer,
} from '@rmwc/image-list';
import '@rmwc/list/styles';

const Search = () => {
  function useQueryParams() {
    return new URLSearchParams(useLocation().search);
  }
  const query = useQueryParams();
  const history = useHistory();

  const searchQuery = gql`
    query {
      search(q: "${query.get('q')}") {
        totalCount
        nodes {
          id
          imageUrl
        }
      }
    }
  `;

  const { error, data } = useQuery(searchQuery, { fetchPolicy: 'no-cache' });

  if (error) return <Error />;

  const stylePlacesThigsList = {
    radius: '4px',
    width: '180px',
    margin: '12px 6px 6px 6px',
  };

  return (
    <>
      {data && data.search && data.search.nodes ? (
        <>
          {data.search?.totalCount !== 0 ? (
            <>
              <Grid>
                <GridCell desktop={12} tablet={12} phone={12}>
                  <ImageList withTextProtection>
                    {data.search?.nodes.map((src) => (
                      <ImageListItem key={src.id} style={stylePlacesThigsList}>
                        <ImageListImageAspectContainer>
                          <ImageListImage
                            src={`${src.imageUrl}?width=200&height=200`}
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
            <>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <img src="/images.svg" width="100%" />
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
              <Grid>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
                <GridCell desktop={4} tablet={4} phone={4}>
                  <center>Sorry, No result found!</center>
                </GridCell>
                <GridCell desktop={4} tablet={4} phone={4}></GridCell>
              </Grid>
            </>
          )}
        </>
      ) : (
        <Loading />
      )}
    </>
  );
};

export default Search;
