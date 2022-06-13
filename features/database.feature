Feature: creating a new database

    Scenario: database is called for 1st time
    Given there is no database file
    When Database is instantiated
    Then Database creates a new database file
