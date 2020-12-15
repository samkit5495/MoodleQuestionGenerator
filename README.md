Moodle Questions Generator
===================

## Description

### Steps to convert excel format to xml format

- First download excel format from <a href="/static/format/Moodle Bulk Import Format.xlsx">here</a>
- Then add questions in different tabs in excel according to question type
- Then upload the excel file here and click on convert
- Save new opened page as xml format and upload into moodle

## Setup
- Install system package. See the `system_package.txt` file. (*Unix)

- Create virtual enviroment (use `virtualenv`) and activate it.

- Then install python packages:  
```
$ pip install -r requirements.txt
```

- Run it:

```
$ python app.py
```

- Go to http://localhost:5000

