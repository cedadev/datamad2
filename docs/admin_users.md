---
layout: default
title: Datamad Documentation
---

# Admin Users

Admins users have access to the datacentre tab in the user dropdown menu. This allows you to:
- Change name of the project used in JIRA for data management
- Add/remove users
- Manage user admin privileges
- The mapping of fields between datamad and JIRA
- Adding document templates for generating documents
- Data formats (for document generation)
- Preservation plans (for document generation)

They also have the ability to add documents in bulk.

![Filter Panel](/assets/images/admin_users/admin_user_menu.png){:.border}

### {% include linked_header.html title="User Management" %}
You can view the users attributed to your datacentre by clicking the users link. This will be prefixed
by the name of your datacentre.

![Filter Panel](/assets/images/admin_users/datacentre_navigation.png){:.border}

Each user is listed with their email address and admin status. There is also the option to edit or remove the users.

#### Adding a new user

1. Click the ![Add User Button](/assets/images/admin_users/add_user_button.png){:.border} button
2. Fill in the form
3. Set a random password. When the user logs in for the first time, they should use the forgotten password
link to set their own password.

#### Promoting a user to admin

1. From the user list, click edit user.
2. Check the box at the bottom of the form which says "admin status".

### {% include linked_header.html title="Connecting to JIRA" %}

The connection to JIRA requires 3 things:

1. A data management JIRA Project (This will be )
2. An issue type ID (This is the id of the issueType model you are using in your project)
3. Mapping between DataMAD and the custom fields in JIRA 

Once theses things are set up, you can use the "Convert to JIRA Ticket" action in the grant actions.
This takes the information in the DataMAD database and creates an issue in JIRA based on the mapping you have setup.

If there is already an issue in JIRA for this grant, DataMAD searches the `summary` field in JIRA for the grant reference.
If a match is found, it will not create a new issue but will get the link to the matched issue and store it in DataMAD for
quick access.

### {% include linked_header.html title="Sub Tasks" %}
...coming soon...


### {% include linked_header.html title="Document Templates" %}

Using the "Generate Document From Template" link in the grant actions list (found on the grant detail page), you can create
a document from a template using fields stored in DataMAD. 

In order to use this feature, you will first need to create a document template. This uses word documents with special [Jinja](https://jinja.palletsprojects.com/en/2.11.x/templates/) 
template tags.

An example document can be found [here](/assets/files/document_template_test.docx) which gives examples for many of the types of things that you might want to do with a document template including:

- formatting
- tables
- variable substitution

This document also lists all the available fields which can be used in your template. This document is used as part of the 
test suite for DataMAD so is regularly checked to make sure that it can generate successfully.

If you wish to use the grant data product feature to generate an initial DMP document, then you might want to setup
some data format and preservation plans. This can be done from the account menu as an admin user. More information about 
data products can be found in the [tutorial](tutorial.html#data-products).

![Filter Panel](/assets/images/admin_users/datacentre_navigation.png){:.border}
 

### {% include linked_header.html title="Bulk Document Uploads" %}

This is primarily for NERC staff to add in the initial grant documents.It can be accessed by following the `Upload Documents` link in the navigation header.

These documents must match the file naming convention to make sure they end up associated with the correct grants.

The convention is:
`<GRANT REFERENCE (underscore separated)>_<DOC TYPE>`
e.g. NE_T000619_1_DMP.pdf

Once you have loaded the page, you will see an area where you can either drag and drop files or use the ![Add Files Button](/assets/images/admin_users/add_files.png) button.

![Filter Panel](/assets/images/admin_users/bulk_document_upload.png){:.border.w-100}

Once you have added some files, you can either upload individual files by clicking their own upload button or upload all by clicking ![Start Upload Button](/assets/images/admin_users/start_upload.png) button.

![Filter Panel](/assets/images/admin_users/files_added.png){:.border.w-100}

Files which fail, either because they don't meet the file naming convention or the file has already been uploaded will display an error message. Successful files will change to show the option to delete and become a link
to allow you to look at them.