# Testing Plan for GUDLFT

This file contains the test plan for GUDLFT.

## All functions atm

- loadClubs() => loads all clubs from the database
- loadCompetitions() => loads all competitions from the database
- index() => Loads the index page. This page allows the user to login to its club account. It will return the list of future competitions (showSummary)
- showSummary() => Loads the summary page. This page shows the user the list of competitions that are going to take place in the future. They can select a competition.
- book() => They can use ther points to buy a ticket in the selected competition. They cannot buy more ticket than the number of available tickets. They can only buy 12 tickets max  per competition.
- purchasePlaces() => They will see the number of tickets they have purchased and/or the completition of the competition. Points used has to be deducted from the user's points.
- logout() => Logs the user out of their club account.


## All tests that I need to implement

### loadClubs() [DONE]

Make a test that checks if the function loads all clubs from the database.
We can make sure we load all clubs by checking the length of the returned array.

### loadCompetitions() [DONE]

Make a test that checks if the function loads all competitions from the database.
We can make sure we load all competitions by checking the length of the returned array.

### index()

Make a test that checks if the template is correctly loaded.
we can make sure the template is loaded by checking if the <title> of the page is correct. [DONE]

Make a test that checks if the page is correctly loaded (status_code_200).
we can make sure the page is loaded by checking if the status code is 200. [DONE]

Make an **happy path** test where the user logs in and is redirected to the summary page.
we can make sure the user is logged in by checking if the user can access the summary page (status_code_200) &  if the welcome message is correct. [DONE]

Make a **sad path** test where the user is unregistered.
we can make sure the user is not logged in by checking if the user is redirected to the index page (status_code_200) &  if an error message is displayed. [DONE]

Make a **sad path** test where the user do not enter an email
we can make sure the user is not logged in by checking if the user is redirected to the index page (status_code_200) &  if an error message is displayed. [DONE]

### showSummary()

Make a test that checks if the template is correctly loaded.
we can make sure the template is loaded by checking if the <title> of the page is correct.

Make a test that checks if the page is correctly loaded (status_code_200).
we can make sure the page is loaded by checking if the status code is 200.

Make a test that check if the competition list is correctly loaded.
we can make sure the competition list is correct by checking the lenght of the returned array & checking the competition dates.


### book()

Make a test that checks if the template is correctly loaded.
we can make sure the template is loaded by checking if the <title> of the page is correct.

Make a test that checks if the page is correctly loaded (status_code_200).
we can make sure the page is loaded by checking if the status code is 200.

Make a  **sad path** test that check if the user trie to book more than the available tickets in the competition. The expected result is an error message.
we can make sure the user cannot book more than the available tickets by checking if the error message is displayed when current_ticket + booked_ticket > available_tickets.

Make a **sad path** test that check if the user tries to book more than 12 tickets. The expected result is an error message.
we can make sure the user cannot book more than 12 tickets by checking if an error message is displayed when 13 tickets are booked.

Make a **happy path** test that check if the user has successfully booked a ticket.
We can make sure the user has successfully booked a ticket by checking if the user is redirected to the summary page (status_code_200) &  if the message is correct.

Make a **sad path** test where the user tries to book a ticket but he has not enough points.
we can make sure the user cannot book a ticket by checking if the user is redirected to the summary page (status_code_200) &  if an error message is displayed.

Make a **sad path** test where the user tries to book a ticket for a competition in the past.
we can make sure the user cannot book a ticket by checking if the user is redirected to the summary page (status_code_200) &  if an error message is displayed.


### purchasePlaces()

Make a **happy path** test that check if the user has successfully booked a ticket and the points are deducted.
We can make sure the user has successfully booked a ticket by checking if the user is redirected to the summary page (status_code_200) &  if the message is correct & if the points are deducted from the user's points.

Make a **happy path** test that check if the user has successfully booked a ticket and the number of tickets is updated.
We can make sure the user has successfully booked a ticket by checking if the user is redirected to the summary page (status_code_200) &  if the message is correct & if the number of tickets is updated.

### logout()
Make a test that makes sure the user is logged out.
we can make sure the user is logged out by checking if the status code is 302.