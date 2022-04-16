"""People Component"""


from utils import get_preview_file_name


class People():
  """Worker People Component"""
  def __init__(self, db):
    self.db = db

  def run(self, event):
    """Run people component"""
    try:
      print(f'executing people component for {get_preview_file_name(event)}')
    except Exception as e:
      print(f'error executing people component: {str(e)}')
    finally:
      print(f'finished executing people component for mediaitem: {event["id"]}')
