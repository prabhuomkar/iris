Feature: MediaItems
  Upload photos and videos to test the basic information, cdn urls, metadata information.

  Scenario Outline: Upload and Validate Metadata
    Given api service is running
    When user uploads "<file_type>" file
    Then file is uploaded
    And metadata "<metadata>" is validated

    Examples: Photos
      | file_type | metadata          |
      | GIF       | image/gif,2080761 |
      | HEIC      | ,107760           |
      | ICO       | ,432254           |
      | JPEG      | image/jpeg,239829 |
      | PNG       | image/png,446687  |
      | TIFF      | ,153116           |
      | WEBP      | image/webp,280032 |
  
  Scenario Outline: Update MediaItem Description
    Given api service is running
    When user updates "<file_type>" file
    Then "<file_type>" file is updated

    Examples: Photos
      | file_type |
      | HEIC      |
      | JPEG      |
      | PNG       |
  
  Scenario Outline: Favourite MediaItems
    Given api service is running
    When user favourites "<file_type>" file
    Then "<file_type>" file is marked as favourite
    And "<file_type>" is listed in favourites

    Examples: Photos
      | file_type |
      | HEIC      |
      | JPEG      |
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
      | JPEG      |
      | PNG       |
