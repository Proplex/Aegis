Feature: database flatfile handling
    Scenario: database is called for 1st time
    Given there is no database file
    When Database is instantiated
    Then Database creates a new database file

    Scenario: a database is loaded from a previous run
    Given there is a database file
    When Database is instantiated
    Then Database loads the contents from the flatfile

