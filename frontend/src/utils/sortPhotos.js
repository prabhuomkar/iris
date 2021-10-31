import moment from 'moment';

const sortPhotos = (obj) => {
  var sortedObj = obj.sort((a, b) => {
    if (moment(a.createdAt) > moment(b.createdAt)) return -1;
    if (moment(a.createdAt) < moment(b.createdAt)) return 1;
    return 0;
  });
  return sortedObj;
};

export default sortPhotos;
