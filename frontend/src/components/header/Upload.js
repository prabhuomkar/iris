import React, { useState } from 'react';
import { Button } from '@rmwc/button';
import { UploadDialog } from './components';
import '@rmwc/button/styles';

const Upload = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <UploadDialog open={open} setOpen={setOpen} />
      <Button
        unelevated
        label="Upload"
        icon="file_upload"
        onClick={() => setOpen(true)}
        style={{ color: '#fff' }}
      />
    </>
  );
};

export default Upload;
