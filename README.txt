# Lab 8 (FINAL)

## Description
This lab was a flask app site with basic login functionality and a few options after logging in. These options have
different output based on the current user's access level, and attempting to access them without being logged in will
result in an appropriate message. A database is used to store the usernames, hashed + salted passwords, and access level
of the user. The site uses bootstrap and jquery, which are protected from XSS attacks with the integrity and
crossorigin attributes. When attempting to log in, the user will have 3 chances before they are permanently locked out
and will be unable to log in even if they use the correct credentials for an account. This is done using sessions from
flask, which allows the server to store information about the current session/browser accessing the site. This is also
how the user remains logged in. When executing SQL queries on the database, it uses parameterized statements to prevent
an SQL injection attack in the input fields.

On account creation, it ensures that the username is not already tied to an account and then checks if the password
is complex enough. If it isn't, it returns an alert informing the user to try again. Alternatively, the user can press
the generate password button, which creates a randomized password of length 8-25 that satisfies those requirements and
inserts it into the input box. Since it was buggy on some browsers with the user not being able to view it, there is
also an alert popup that displays the generated password. After successfully creating an account the user can log in
by navigating with the forward and back keys of their browser, or the nav at the top of the page. If they are logged in,
most pages will inform the user with an alert at the top showing their username. The user can switch accounts at any
time by logging in to a new one and that will overwrite the account stored in the session.

## Setup Instructions
1. Ensure that these files exist in these directories
    * static
        * globe.jpg
        * style.css
    * templates
        * create_account.html
        * home.html
        * login.html
        * successful_login.html
    * account.db - not necessary on first run
    * app.py
    * helpers.py
    * setup.py
2. Run setup.py to create the database and table necessary to store passwords. It will also insert 3 predefined accounts
   and print out the table to the console to ensure it was properly set up.
3. Run app.py and go to the link/server
4. Enjoy!

## Testing Instructions
### Getting locked out
1. Run the flask app
2. Navigate to the login page
3. Try to log in using some random, invalid credentials
    * ie. "sdfsadf", "12345"
4. Repeat this 2 more times
5. You will see a warning alert and you will no longer be able to successfully log in
6. Attempt to log in using valid credentials
    * "Dave", "123"
    * It will not let you log in, you will need to restart the flask app
### Creating a new account
7. Rerun the flask app
8. Navigate to the create account page
9. Type in a username and weak password
    * It will tell you that the password was not strong enough
10. Press the generate password button (copy the password for later use)
11. Retype your account name and submit
    * Success message
### Logging in
12. Navigate to the login page
13. Enter your username and copied password
14. On the success page, you will see some options. The only one you have access to is time reporting, all the others
   will say you don't have access (This is done by displaying a paragraph tag with appropriate output)
### Switching accounts
15. Return to the login page
16. Log in using "Dave" for the username and "123" for the password
17. On the success page, you will be able to access all of the options.