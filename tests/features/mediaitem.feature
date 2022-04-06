Feature: MediaItems
  Upload photos and videos to test the basic information, cdn urls, metadata information.

  Scenario Outline: Upload and Validate Metadata
    Given api service is running
    When user uploads "<file_type>" file
    Then file is uploaded
    And metadata "<metadata>" is validated

    Examples: Photos
      | file_type | metadata            |
      | GIF       | image/gif,2080761   |
      | HEIC      | image/heic,107760   |
      | ICO       | image/x-icon,432254 |
      | JPEG      | image/jpeg,239829   |
      | PNG       | image/png,446687    |
      | WEBP      | image/webp,280032   |
  
  Scenario Outline: Update MediaItem Description
    Given api service is running
    When user updates "<mime_type>" file
    Then file description is updated

    Examples: Photos
      | file_type | mime_type  |
      | JPEG      | image/jpeg |
      | PNG       | image/png  |
  
  Scenario Outline: Favourite MediaItems
    Given api service is running
    When user favourites "<mime_type>" file
    Then file is marked as favourite
    And file is listed in favourites
    When user unfavourites "<mime_type>" file
    Then file is not marked as favourite
    And file is not listed in favourites

    Examples: Photos
      | file_type | mime_type  |
      | JPEG      | image/jpeg |
      | PNG       | image/png  |
  
  Scenario Outline: Delete MediaItems
    Given api service is running
    When user deletes "<mime_type>" file
    Then file is marked as deleted
    And file is listed in trash
    When user undeletes "<mime_type>" file
    Then file is not marked as deleted
    And file is not listed in trash
    When user permanently deletes "<mime_type>" file
    Then file is deleted
    And file is not listed in trash

    Examples: Photos
      | file_type | mime_type  |
      | JPEG      | image/jpeg |
      | PNG       | image/png  |
