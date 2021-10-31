import React, { useState } from 'react';
import { TopAppBarSection } from '@rmwc/top-app-bar';
import { Button } from '@rmwc/button';
import '@rmwc/button/styles';
import UploadDialog from '../UploadDialog';

const Upload = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <UploadDialog open={open} setOpen={setOpen} />
      <TopAppBarSection alignEnd>
        <Button
          outlined
          label="Upload"
          icon="file_upload"
          onClick={() => setOpen(true)}
        />
      </TopAppBarSection>
    </>
  );
};

export default Upload;
