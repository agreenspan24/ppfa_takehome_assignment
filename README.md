***Please see the project_review.md file for a summary report on the project's development.***

# Required software
- python3
- pip
- virtualenv
- sqlite3

# Installation
    $ virtualenv -p python3 venv
    $ source venv/bin/activate
    $ pip install -e .
    $ pip install -r requirements.txt

# Run migrations and start app
    $ manage.py migrate
    $ manage.py runserver

In a separate terminal from the server:
    $ source venv/bin/activate (if not already in venv)
    $ manage.py test

You should see an error in the server terminal after running tests.

# Project requirements

This project is meant to be completed in two hours or less. Submitting it partially complete is fine if you run out of time. And please provide feedback on the project if you have any.

## Part 1: Appointments REST endpoints
1. create a new git branch called appoinments
2. complete the serializers for appointments (in pp.appointments.serializers)
3. write some tests for the endpoints (pp.appointments.tests). You should fill out the existing ones, and add 2-3 tests for edge cases.
4. add the ability to filter appointments by date for the list view. the filtering should be done in the querystring. i.e. (urlencoded of course):

    `GET /api/v1/appointments/?start_date=07-11-2020&end_date=09-20-2020`

## Part 2

1. Create a new branch from appointments (not master) called doctors
2. Create a new app called 'doctors'

    `mkdir pp/doctors`
    `$ manage.py startapp doctors pp/doctors`

3. The doctor model should contain the following data:
    - Name
    - Specialization (you can limit it to 5 options. e.g. podiatrist, cardiologist, etc...)
    - Rating (1-5)

4. create a many-to-many relation between the doctors model and the appointments model.

5. Modify the appointments serializer and tests. You should now be able to add a doctor when you create an appointment. You should add logic to check that a doctor does not have an existing appointment in the slot you are creating.

For the purpose of this exercise, you can assume all appointments start on the hour, and only run for one hour.