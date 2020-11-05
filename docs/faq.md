---
layout: default
title: DataMAD Documentation
---

# FAQ


### {% include linked_header.html title="JIRA Convert Issues" %}

```
There was an error when trying to create the JIRA issue. Operation value must be a...
```

This is caused when the mapped field from DataMAD presents a data type to JIRA which is not compatible.
For example the error message `Operation value must be a string` means that one of your mapped fields is expecting
a string but is getting something else. The first place to check is your JIRA Issue Fields mapping at `/account/datacentre/jira-issue`.
Each of the fields tells you what data type it will present to JIRA in the help text below the relevant field. 

![Help Text](/assets/images/faq/data_type_helptext.png){:.border}

Make sure that all the fields you have mapped to in JIRA accept the data type mentioned in this string.

