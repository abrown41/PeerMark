===============
Peer Mark
===============

Python package for creating/grading peer assessment projects

* Free software: 3-clause BSD license

Features
--------

`peer_mark` provides two command line utilities for setting and grading peer
review assessments for group projects on canvas

You will need a canvas API token: canvas>account>settings>approved
integrations>generate new access token), and the utility will prompt you to
provide the canvas url and access token on first run.

`generate_peer` produces spreadsheets for completion by students working in
groups. The utility pulls team information from canvas  If the access token is available, you will be shown a list
of all your canvas courses for selection, and once a course is selected, you
will be shown a list of all available groups sets. Simply select the correct
group set, and the spreadsheets will be generated and uploaded to the groups'
home pages in the files section. If you have a very long list of canvas modules,
you can restrict the review by providing a semester string:

    generate_peer -s 2251

will show only courses active in the 25/26 AY, for instance. Or if you know the
canvas course ID, it can be provided directly and you can skip the selection of
the course:

    generate_peer -c 32732

`extract_peer` will prompt you with to select a canvas course, and then to
select the assignment you wish to grade. This will be the assignment to which
the students submitted their peer assessment spreadsheets. Simply select the
correct assignment and the script will download the uploaded spreadsheets,
collate the marks for each students, insert the mark in the canvas gradebook,
and upload the collated feedback for each student as a comment on their
assignment submission.
