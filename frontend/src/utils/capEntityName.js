const capEntityName = (things) => {
  if (things !== '' && things !== ' ') {
    const words = things.trim().split(' ');

    return words
      .map((word) => {
        return word[0].toUpperCase() + word.substring(1);
      })
      .join(' ');
  }
};

export default capEntityName;
