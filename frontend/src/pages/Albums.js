import React from 'react';
import Box from '@mui/material/Box';
import ImageListItem, {
  imageListItemClasses,
} from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import Divider from '@mui/material/Divider';
import {
  AlbumAction,
  AlbumFormDialog,
  CreateAlbum,
} from '../components/albums';
import AlbumsStyled from '../components/albums/styles';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  breakpoints: {
    values: {
      mobile: 0,
      bigMobile: 350,
      tablet: 650,
      desktop: 900,
    },
  },
  typography: {
    fontFamily: `"Poppins", sans-serif`,
  },
});

const Albums = () => {
  return (
    <>
      <AlbumsStyled>
        <div className="albums-heading">
          <div className="albums-title">Albums</div>
          <div>
            <CreateAlbum />
          </div>
        </div>
        <Divider />
        <ThemeProvider theme={theme}>
          <Box
            sx={{
              marginTop: '10px',
              display: 'grid',
              gridTemplateColumns: {
                mobile: 'repeat(1, 1fr)',
                bigMobile: 'repeat(2, 1fr)',
                tablet: 'repeat(3, 1fr)',
                desktop: 'repeat(5, 1fr)',
              },
              [`& .${imageListItemClasses.root}`]: {
                display: 'flex',
                flexDirection: 'column',
                margin: '6px',
              },
            }}
          >
            {itemData.map((item) => (
              <ImageListItem key={item.img} className="albums-image-list">
                <img
                  src={`${item.img}?w=164&h=164&fit=crop&auto=format`}
                  srcSet={`${item.img}?w=164&h=164&fit=crop&auto=format&dpr=2 2x`}
                  alt={item.title}
                  loading="lazy"
                  style={{ borderRadius: '6px' }}
                />
                <div className="albums-more">
                  <AlbumAction />
                  <AlbumFormDialog />
                </div>
                <ImageListItemBar
                  title={item.title}
                  subtitle={
                    <div
                      style={{
                        fontSize: '13px',
                        color: '#5f6368',
                      }}
                    >
                      6 items
                    </div>
                  }
                  position="below"
                />
              </ImageListItem>
            ))}
          </Box>
        </ThemeProvider>
      </AlbumsStyled>
    </>
  );
};

export default Albums;

const itemData = [
  {
    img: 'https://images.unsplash.com/photo-1551963831-b3b1ca40c98e',
    title: 'Breakfast',
    author: '@bkristastucchio',
  },
  {
    img: 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d',
    title: 'Burger',
    author: '@rollelflex_graphy726',
  },
  {
    img: 'https://images.unsplash.com/photo-1522770179533-24471fcdba45',
    title: 'Camera',
    author: '@helloimnik',
  },
  {
    img: 'https://images.unsplash.com/photo-1444418776041-9c7e33cc5a9c',
    title: 'Coffee',
    author: '@nolanissac',
  },
  {
    img: 'https://images.unsplash.com/photo-1533827432537-70133748f5c8',
    title: 'Hats',
    author: '@hjrc33',
  },
  {
    img: 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62',
    title: 'Honey',
    author: '@arwinneil',
  },
  {
    img: 'https://images.unsplash.com/photo-1516802273409-68526ee1bdd6',
    title: 'Basketball',
    author: '@tjdragotta',
  },
  {
    img: 'https://images.unsplash.com/photo-1518756131217-31eb79b20e8f',
    title: 'Fern',
    author: '@katie_wasserman',
  },
  {
    img: 'https://images.unsplash.com/photo-1597645587822-e99fa5d45d25',
    title: 'Mushrooms',
    author: '@silverdalex',
  },
  {
    img: 'https://images.unsplash.com/photo-1567306301408-9b74779a11af',
    title: 'Tomato basil',
    author: '@shelleypauls',
  },
  {
    img: 'https://images.unsplash.com/photo-1471357674240-e1a485acb3e1',
    title: 'Sea star',
    author: '@peterlaster',
  },
  {
    img: 'https://images.unsplash.com/photo-1589118949245-7d38baf380d6',
    title: 'Bike',
    author: '@southside_customs',
  },
];
