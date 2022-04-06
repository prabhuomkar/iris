Feature: Albums
  Select photos or videos and create albums

  Scenario Outline: Upload MediaItems for Albums
    Given api service is running
    When user uploads "<file_type>" file
    Then file is uploaded

    Examples: Photos
      | file_type | 
      | GIF       | 
      | HEIC      | 
      | ICO       | 
      | JPEG      | 
      | PNG       | 
      | WEBP      | 

  Scenario: Create Album
    Given api service is running
    When user creates an album
    Then album is created
    And album is listed in albums
  
  Scenario: Update Album
    Given api service is running
    When user updates an album
    Then album is updated
  
  Scenario: Update Album MediaItems
    Given api service is running
    When user updates an album mediaitems
    Then album mediaitems are updated

  Scenario: Update Album Thumbnail
    Given api service is running
    When user updates an album thumbnail
    Then album thumbnail is updated
  
  Scenario: Delete Album
    Given api service is running
    When user deletes an album
    Then album is deleted
    And album is not listed in albums
