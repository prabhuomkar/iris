import { styled } from '@mui/system';

const AlbumsStyled = styled('div')({
  '.albums-heading': {
    marginBottom: '10px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },

  '.albums-title': {
    fontSize: '17px',
  },

  '.albums-image-list': {
    position: 'relative',
  },

  '.albums-more': {
    position: 'absolute',
    top: '5px',
    right: '0px',
    cursor: 'pointer',
    color: '#ffffff',
  },

  '.album-dialog': {
    display: 'flex',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
});

export default AlbumsStyled;
