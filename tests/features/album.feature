Feature: Albums
  Select photos or videos and create albums

  Scenario: List Albums
    Given api service is running
    When user requests for albums
    Then no albums are found

  Scenario: Create Album
    Given api service is running
    When user creates an album
    Then album is created
    And mediaitems are listed in album
  
  Scenario: List Albums
    Given api service is running
    When user requests for albums
    Then albums are found

  Scenario: Single Album
    Given api service is running
    When user requests for album
    Then album is viewed
    And mediaitems are listed in album
  
  Scenario: Updates Album
    Given api service is running
    When user updates an album
    Then album is updated
    And mediaitems are listed in album
  
  Scenario: Updates Album MediaItems
    Given api service is running
    When user updates an album mediaitems
    Then album is updated
    And mediaitems are listed in album

  Scenario: Updates Album Thumbnail
    Given api service is running
    When user updates an album thumbnail
    Then album thumbnail is updated
    And mediaitems are listed in album
  
  Scenario: Delete Album
    Given api service is running
    When user deletes an album
    Then album is deleted
    And mediaitems are listed in album
