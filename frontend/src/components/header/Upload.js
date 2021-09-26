import React, { useState } from 'react';
import { TopAppBarActionItem } from '@rmwc/top-app-bar';
import UploadDialog from '../UploadDialog';

const Upload = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <UploadDialog open={open} setOpen={setOpen} />
      <TopAppBarActionItem icon="file_upload" onClick={() => setOpen(true)} />
    </>
  );
};

export default Upload;
