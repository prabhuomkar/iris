import moment from 'moment';

const reducePhotos = (data) => {
  let output = data.reduce((ob, cur) => {
    let occurs = ob.reduce((n, item, i) => {
      return moment(item.mediaMetadata?.creationTime || item.createdAt).format(
        'D MMMM YYYY'
      ) ===
        moment(cur.mediaMetadata?.creationTime || cur.createdAt).format(
          'D MMMM YYYY'
        )
        ? i
        : n;
    }, -1);

    if (occurs >= 0) {
      ob[occurs].thumbnailUrl = ob[occurs].thumbnailUrl.concat(cur.thumbnailUrl);
      ob[occurs].id = ob[occurs].id.concat(cur.id);
    } else {
      let obj = {
        createdAt: cur.mediaMetadata?.creationTime || cur.createdAt,
        id: [cur.id],
        thumbnailUrl: [cur.thumbnailUrl],
      };
      ob = ob.concat([obj]);
    }
    return ob;
  }, []);
  return output;
};

export default reducePhotos;
