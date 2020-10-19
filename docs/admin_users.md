---
layout: default
title: Datamad Documentation
---

# Admin Users

Admins users have access to the datacentre tab in the user dropdown menu. This allows you to:
- The name of the project used in JIRA for data management
- Add/remove users
- Manage user admin privileges
- The mapping of fields between datamad and JIRA
- Adding document templates for generating documents
- Data formats (for document generation)
- Preservation plans (for document generation)

They also have the ability to add documents in bulk.

![Filter Panel](/assets/images/admin_users/admin_user_menu.png){:.border}

## {% include linked_header.html title="Adding New Users" %}
...coming soon...

## {% include linked_header.html title="Connecting to JIRA" %}
...coming soon...


## {% include linked_header.html title="Sub Tasks" %}
...coming soon...


## {% include linked_header.html title="Document Templating" %}
...coming soon...


## {% include linked_header.html title="Bulk Document Uploads" %}

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