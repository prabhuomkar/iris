Feature: MediaItems
  Upload photos and videos to test the basic information, cdn urls, metadata information.

  Scenario Outline: Upload and Validate Metadata
    Given api service is running
    When user uploads a "<file_type>" file
    Then "<file_type>" file is uploaded
    And metadata for "<file_type>" file is validated

    Examples: Photos
      | file_type |
      | BMP       |
      | GIF       |
      | HEIC      |
      | ICO       |
      | JPG       |
      | PNG       |
      | TIFF      |

    Examples: Videos
      | file_type |
      | MOV       |
