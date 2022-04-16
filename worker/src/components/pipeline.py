"""Pipeline"""
import os
from threading import Thread

from utils import download_mediaitem, get_details_from_event, get_source_file_name, get_preview_file_name
from .metadata import Metadata
from .places import Places
from .people import People
from .things import Things


class Pipeline():
  """Worker Pipeline"""
  def __init__(self, db):
    self.db = db
    self.components = {
      'metadata': Metadata(db),
      'places': Places(db),
      'people': People(db),
      'things': Things(db)
    }

  def execute_components(self, event_details):
    """Start executing pipeline components"""
    threads = []
    threads.append(Thread(target=self.components['metadata'].run, args=(event_details,)))
    if 'places' in event_details['components']:
      threads.append(Thread(target=self.components['places'].run, args=(event_details,)))
    [thread.start() for thread in threads] # pylint: disable=expression-not-assigned
    [thread.join() for thread in threads] # pylint: disable=expression-not-assigned
    inference_threads = []
    if 'people' in event_details['components']:
      inference_threads.append(Thread(target=self.components['places'].run, args=(event_details,)))
    if 'things' in event_details['components']:
      inference_threads.append(Thread(target=self.components['things'].run, args=(event_details,)))
    [thread.start() for thread in inference_threads] # pylint: disable=expression-not-assigned
    [thread.join() for thread in inference_threads] # pylint: disable=expression-not-assigned

  def process(self, event):
    """Drives pipeline processing"""
    # extract event details
    event_details = get_details_from_event(event)
    if len(event_details.keys()) > 0:
      event_details['source_filename'] = get_source_file_name(event_details)
      event_details['preview_filename'] = get_preview_file_name(event_details)
      # download mediaitem
      mediaitem_downloaded = download_mediaitem(event_details['download_url'], event_details['source_filename'])
      # execute components
      if mediaitem_downloaded:
        print(f'downloading mediaitem file: {event_details["source_filename"]}')
        self.execute_components(event_details)
        # delete downloaded mediaitems
        if os.path.exists(event_details['source_filename']):
          os.remove(event_details['source_filename'])
        if os.path.exists(event_details['preview_filename']):
          os.remove(event_details['preview_filename'])
