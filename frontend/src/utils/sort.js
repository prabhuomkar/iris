import moment from 'moment';

const sort_photos = (obj) => {
  var sorted_photos = obj.sort((a, b) => {
    if (moment(a.createdAt) > moment(b.createdAt)) return -1;
    if (moment(a.createdAt) < moment(b.createdAt)) return 1;
    return 0;
  });
  return sorted_photos;
};

export default sort_photos;
