# Project Review - PPFA Backend Challenge

Adam Greenspan - April 7, 2021

## Setup
Setup was fairly straightforward, with only two minor hiccups. The first was a weird bug that occurred because appointments/apps.py didn't name the config "pp.appointments", just "appointments". Fixed this relatively easily, but the bug wasn't very helpful. There was also a "BigAutoField" warning that I cleaned up as well. Also, a minor update on the instructions for running tests: you also need to start the virtual environment in the second terminal window for running tests (i.e. run `source venv/bin/activate`). 

## Part One
For the serializers work, I found that existing serializer worked just fine for the context of appointments. It mapped fields from the API directly to their model counterparts, with validation built in. The only thing I could think of that would be worthwhile to modify there would be accepting the long form versions of the appointment reasons ("Annual Checkup" instead of "CH"). Yet, ultimately if the client-side is configured correctly, any select input should be using the two-character value behind the scenes anyway, so it's harder to misspell. So, maybe I'm missing something here. I'm happy to go back to the project to fix it later.

In addition to building out all the tests prompted, I also added two tests during this step: `test_update_appointment` and `test_get_appointments_filtered`. These just helped cover the rest of the functionality. At setup and teardown, I fetch and delete any existing appointments, so each test is running with a clean slate. I also built wrappers behind each CRUD operation, so their logic was abstracted away from the tests.

For filtering by date, I add them to the query params and filter at the database level using Django's ORM features. As mentioned above, this is covered by testing as well.

## Part Two
For part two, I created the Doctor model with the specified fields and a many-to-many relationship with appointments.

The main challenge here was modifying the serializer to add doctors and linkages between doctors and appointments. For each new doctor on an appointment, we first find or create that doctor's record in the database. From there, we check if any of those doctors have a conflicting an appointment. Finally, for existing appointments, we remove the doctors who were not on the most recent update, assuming that they have been deleted. 

This more complicated logic is encompassed in the following tests: `test_add_appointment_with_doctor`, `test_add_doctor_to_existing_appointment`, `test_remove_doctor_from_existing_appointment`, and `test_add_doctor_conflicting_appointments`. While I think these provide good coverage, it would be helpful to create additional tests around the logic of conflicting appointments. I was running out of time by this point and wanted to make sure I finished in a reasonable time frame. 

## Summary
Overall, this was a fun challenge for me! I really love being able to do test-driven development like this. I completed this over about three hours on Wednesday, April 7, working in a couple increments throughout the afternoon. 

If I had more time, I mentioned above there would be more tests around the conflicting appointment schedule. I would also have done more around accommodating different versions of appointment reasons in serialization. I didn't build out an API for doctors, because it wasn't part of the requirements, but it would eventually be useful. Finally, as this app grew, more consolidation and simplifications around the views' logic behind objects not found and validation errors would be nice. Of course, no back-end exists in isolation, there would also be many more changes depending on front-end set-up. 

