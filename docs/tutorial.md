---
layout: default
title: Datamad - Getting Started
---

# Getting Started

This page should contain all the information you need to get started with using DataMAD.

### {% include linked_header.html title="Finding Grants" %}

On the left hand side of the screen is the filter panel. This comprises of a search box, where you can use free text queries to 
find specific terms and phrases and categories which you can use to narrow your search.

The sections below describe how to use these features.

![Filter Panel](/assets/images/tutorial/Filter_panel.png){:.border}

#### {% include linked_header.html title="Search Box" %}

The search box can be used for free text queries. The fields that this search box will look at when determining your results are:
- Title
- Abstract
- Grant Reference
- Grant Holder or PI
- Department
- Research Organisation
- Parent_grant (Reference and Title)
- Facility
- Call

![Search Box](/assets/images/tutorial/search_box.png){:.border}

The search capabilities are handled by [Django Haystack](https://django-haystack.readthedocs.io/en/master/) and this provides a
basic query syntax.

Full grant references can be searched to return exact grants.

"`-`" Can be used to `NOT` a term. e.g. `ocean -atmosphere` would construct the search looking for `ocean AND NOT atmosphere`

Remaining terms will be `AND`ed together.



### {% include linked_header.html title="Grant Documents" %}

Grant documents are linked to grants and can be found on the grant detail page. You access the grant details by clicking on
the grant reference from the home page.
![Grant Example](/assets/images/tutorial/grant_table.png){:.border.w-100}

The documents can be found on the right of the detail page underneath the quick links and grant actions.

![Grant Actions](/assets/images/tutorial/grant_toolbar.png){:.border}

Grant documents can be uploaded by clicking the "Add Document" button.
There are strict criteria for the naming convention. This is so that the documents get 
assigned the correct type (e.g. DMP or supporting document) and are assigned to the correct grant.

![Document Upload](/assets/images/tutorial/document_upload.png){:.border.w-100}

Adding tags to the uploaded document allows you to add extra context which will be displayed
alongside the filename in the grant detail page.

### {% include linked_header.html title="User Preferences" %}

User preferences can be accessed from the user dropdown menu in the top right.

![Preferences Menu](/assets/images/tutorial/Preferences_Menu.png){:.border}

#### {% include linked_header.html title="Preferred Filters" %}

Each individual has their own workflow which will make some filters more important than others. You can hide 
filters which are not important to you by selecting your preferred filters. This will hide criteria which is not important to your
workflow and provide you with smaller number of filter categories.

If you haven't saved any preferences then all will be available and there is a link at the bottom of the filter panel which 
takes you to the form to select your preferred filters.

Once you have selected your preferred filters, you will need to access them via the user menu.



#### {% include linked_header.html title="Perferred Sort Method" %}

Some workflows might lean towards a particular sort order and it could be annoying to have to keep selecting the same sort order, if
your common use case is not to search in the search bar. By default, it sorts by relevance to your search, as calculated by the search database. 
You can set the default sort order in your preferences.

### {% include linked_header.html title="Data Products" %}

Data products are used as part of [document templating](#document-templating). You can use this page to document and store different
data products which are to be produced by the data producer.

The possible data products are:

- Digital
- Model Source
- Physical
- Hardcopy
- Third Party

These can then be auto-templated into a document e.g. DMP 


### {% include linked_header.html title="Document Templating" %}

Document templating can be used to generate documents from the DataMAD grant, using templates. This could be used
to generate a Data Management Plan.

The button is found in the toolbar on the right when looking at the grant detail page **Generate Document**.

![Grant Actions](/assets/images/tutorial/grant_actions.png){:.border}

Document templates come in the form of word documents with special template syntax. More information about writing templates, 
the available variables you can use in your templates, as well as an [example dmp document template](/assets/files/ceda_dmp_template.docx), are found in the [admin](/admin_users#document-templates) pages 