import moment from 'moment';

const reducePhotos = (data) => {
  var output = data.reduce((ob, cur) => {
    // Get the index of the key-value pair.
    var occurs = ob.reduce((n, item, i) => {
      return moment(item.createdAt).format('D MMMM YYYY') ===
        moment(cur.createdAt).format('D MMMM YYYY')
        ? i
        : n;
    }, -1);

    // If date is same
    if (occurs >= 0) {
      // append imageUrl in array
      ob[occurs].imageUrl = ob[occurs].imageUrl.concat(cur.imageUrl);
      ob[occurs].id = ob[occurs].id.concat(cur.id);
    } else {
      // add the imageUrl to ob (but make sure the value is an array).
      var obj = {
        createdAt: cur.createdAt,
        id: [cur.id],
        imageUrl: [cur.imageUrl],
      };
      ob = ob.concat([obj]);
    }
    return ob;
  }, []);
  return output;
};

export default reducePhotos;
