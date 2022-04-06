Feature: MediaItems
  Upload photos and videos to test the basic information, cdn urls, metadata information.

  Scenario Outline: Upload and Validate Metadata
    Given api service is running
    When user uploads "<file_type>" file
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
  
  Scenario Outline: Update MediaItem Description
    Given api service is running
    When user updates "<file_type>" file
    Then "<file_type>" file is updated

    Examples: Photos
      | file_type |
      | HEIC      |
      | JPG       |
      | PNG       |
  
  Scenario Outline: Favourite MediaItems
    Given api service is running
    When user favourites "<file_type>" file
    Then "<file_type>" file is marked as favourite
    And "<file_type>" is listed in favourites

    Examples: Photos
      | file_type |
      | HEIC      |
      | JPG       |
      | PNG       |
  
  Scenario Outline: Delete MediaItems
    Given api service is running
    When user deletes "<file_type>" file
    Then "<file_type>" file is marked as deleted
    And "<file_type>" is listed in trash
    When user permanently deletes "<file_type>" file
    Then "<file_type>" file is deleted
    And "<file_type>" is not listed in trash

    Examples: Photos
      | file_type |
      | HEIC      |
      | JPG       |
      | PNG       |
