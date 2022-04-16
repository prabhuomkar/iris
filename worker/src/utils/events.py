"""Event Utils"""
import json


def get_details_from_event(event):
  """Extracts details from rabbitmq message"""
  try:
    data = json.loads(event)
    return {
      'id': data['id'] if 'id' in data else None,
      'filename': data['fileName'] if 'fileName' in data else None,
      'download_url': data['mediaItem']['downloadUrl'] if 'mediaItem' in data and 'downloadUrl' in data['mediaItem'] else None,
      'components': data['actions'] if 'actions' in data else [],
    }
  except Exception as e:
    print(f'error getting event details: {str(e)}')
  return {}

def get_source_file_name(event):
  """Return filename to save the downloaded mediaitem"""
  return f'mediaitem-{event["id"]}-{event["filename"]}'

def get_preview_file_name(event):
  """Return filename to save the preview mediaitem"""
  return f'{get_source_file_name(event)}.jpg'
