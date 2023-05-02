Feature: The product team service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name    | available | category    | like | color   | size  | create_date | last_modify_date |
        | milk    | True      | GROCERIES   | 0    | PINK    | S     | 2020-03-23  | 2023-02-10       |
        | candy   | False     | GROCERIES   | 2    | OTHER   | L     | 2012-12-14  | 2021-01-19       |
        | shorts  | False     | FASHION     | 10   | BLUE    | M     | 2023-02-18  | 2023-04-01       |
        | pot     | True      | HOME        | 5    | YELLOW  | M     | 2019-08-30  | 2022-03-12       |
        | bear    | True      | ACCESSORIES | 2    | OTHER   | S     | 2018-04-22  | 2023-02-22       |
        | milk    | False     | GROCERIES   | 3    | WHITE   | S     | 2022-10-19  | 2023-03-15       |
        | pot     | True      | HOME        | 4    | WHITE   | XL    | 2021-05-23  | 2022-12-20       |
        | milk    | True      | GROCERIES   | 44   | WHITE   | XS    | 2019-04-29  | 2023-04-03       |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo RESTful Service" in the title
    And I should not see "404 Not Found"


Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Laptop"
    And I select "Device" in the "Category" dropdown
    And I select "True" in the "Available" dropdown
    And I set the "Like" to "8" 
    And I select "Black" in the "Color" dropdown
    And I select "L" in the "Size" dropdown
    And I set the "Create_date" to "04-25-2023"
    And I set the "Last_modify_date" to "04-25-2023"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Laptop" in the "Name" field
    And I should see "8" in the "Like" field
    And I should see "Device" in the "Category" dropdown
    And I should see "True" in the "Available" dropdown
    And I should see "Black" in the "Color" dropdown
    And I should see "L" in the "Size" dropdown
    And I should see "2023-04-25" in the "Create_date" field
    And I should see "2023-04-25" in the "Last_modify_date" field


Scenario: Like a Product
    When I visit the "home page"
    And I set the "Name" to "Banana"
    And I select "Groceries" in the "Category" dropdown
    And I select "True" in the "Available" dropdown
    And I set the "Like" to "3" 
    And I select "Yellow" in the "Color" dropdown
    And I select "S" in the "Size" dropdown
    And I set the "Create_date" to "04-26-2023"
    And I set the "Last_modify_date" to "04-26-2023" 
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I paste the "Id" field
    And I press the "Like" button
    Then I should see the message "The product has been liked!"
    And I should see "4" in the "Like" field


Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "candy" in the results
    And I should see "milk" in the results
    And I should not see "strawberry" in the results
    

Scenario: Search for milk
    When I visit the "Home Page"
    And I set the "Name" to "milk"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "milk" in the results
    And I should not see "kitty" in the results
    And I should not see "leo" in the results


Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "shorts"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "shorts" in the "Name" field
    And I should see "FASHION" in the "Category" field
    When I change "Name" to "jeans"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "jeans" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "jeans" in the results
    And I should not see "shorts" in the results