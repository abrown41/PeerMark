To execute this test, run

<path to python3> <path to PeerMark repository>/source/extract_peer.py 

it should give you the marks_master spreadsheet, and a feedback directory
containing the markdown feedback files. To check if you can generate the PDF
feedback files, change the pdfoutput option in source/extract_peer.py to True.
The feedback directory will then contain PDF files instead of markdown.
