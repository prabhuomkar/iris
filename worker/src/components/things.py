"""Things Component"""


from utils import get_preview_file_name


class Things():
  """Worker Things Component"""
  def __init__(self, db):
    self.db = db

  def run(self, event):
    """Run things component"""
    try:
      print(f'executing things component for {get_preview_file_name(event)}')
    except Exception as e:
      print(f'error executing things component: {str(e)}')
    finally:
      print(f'finished executing things component for mediaitem: {event["id"]}')
