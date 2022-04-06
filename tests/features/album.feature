Feature: Albums
  Select photos or videos and create albums

  Scenario: Create Album
    Given api service is running
    When user creates an album
    Then album is created
    And mediaitems are listed in albums
  
  Scenario: Updates Album
    Given api service is running
    When user updates an album
    Then album is updated
    And mediaitems are listed in albums
  
  Scenario: Updates Album MediaItems
    Given api service is running
    When user updates an album mediaitems
    Then album is updated
    And mediaitems are listed in albums
  
  Scenario: Delete Album
    Given api service is running
    When user deletes an album
    Then album is deleted
    And mediaitems are listed in albums
