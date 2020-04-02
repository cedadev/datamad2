from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


# class GrantQuerySet(models.query.QuerySet):
#     def get(self, **kwargs):
#         return super().get(**kwargs)

# class GrantManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().update(updated_imported_grant=True)

class Grant(models.Model):

    # objects = GrantManager()

    # Grant Reference	Siebel	Unique identifier for the grant			GRANTREFERENCE
    grant_ref = models.CharField(max_length=50, default='', blank=True)
    # alt data contact email
    alt_data_contact = models.CharField(max_length=256, null=True, blank=True)
    # Alt Data Contact Email	Sharepoint	PI may not always be the contact for data related issues (although responsible for ensuring delivery of the data)
    alt_data_contact_email = models.EmailField(null=True, blank=True)
    # Alt Data Contact Phone No	Sharepoint	PI may not always be the contact for data related issues (although responsible for ensuring delivery of the data)
    alt_data_contact_phone = models.CharField(max_length=256, null=True, blank=True)
    # Assigned Data Centre	Sharepoint	E.g. NGDC
    assigned_data_centre = models.CharField(max_length=200, blank=True, null=True,
                                            choices=(
                                                ("BODC", "BODC"),
                                                ("CEDA", "CEDA"),
                                                ("EIDC", "EIDC"),
                                                ("NGDC", "NGDC"),
                                                ("PDC", "PDC"),
                                                ("ADS", "ADS"),
                                            ))
    # Other DC's Expecting Datasets	Sharepoint	E.g. PDC
    other_data_centre = models.CharField(max_length=200, blank=True, null=True,
                                         choices=(
                                             ("BODC", "BODC"),
                                             ("CEDA", "CEDA"),
                                             ("EIDC", "EIDC"),
                                             ("NGDC", "NGDC"),
                                             ("PDC", "PDC"),
                                             ("ADS", "ADS"),
                                         ))
    # Hide Record	Sharepoint
    hide_record = models.BooleanField(null=True, blank=True)
    # DateContact with PI	Sharepoint	Date or Null
    date_contacted_pi = models.DateField(null=True, blank=True)
    # Will Grant Produce Data	Sharepoint	Y/N
    will_grant_produce_data = models.BooleanField(null=True, blank=True)
    # Datasets Delivered as per DMP?	Sharepoint	Yes, No or Null
    datasets_delivered = models.BooleanField(null=True, blank=True,
                                             help_text="Datasets Delivered as per DMP?")
    # Sanctions Recommended	Sharepoint	Yes, No or Null
    sanctions_recommended = models.BooleanField(null=True, blank=True)
    # C for S found?	Sharepoint	Yes/No/Grant not found
    case_for_support_found = models.BooleanField(null=True, blank=True)
    # claim status
    claimed = models.BooleanField(null=True, blank=True)
    # checks for updated imported grant (more than one version)
    updated_imported_grant = models.BooleanField(null=True, blank=True, editable=False, verbose_name='Grant updated')

    # programme - one programme can have many grants
    # programme = models.ForeignKey(to='dmp.Programme', blank=True, null=True, on_delete=models.PROTECT)

    science_area = models.CharField(max_length=256, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.assigned_data_centre is None:
            self.claimed = False
        else:
            self.claimed = True
        return super(Grant, self).save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     if self.importedgrant_set.count() > 1:
    #         self.updated_imported_grant = True
    #     else:
    #         self.updated_imported_grant = False
    #     return super(Grant, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.grant_ref}"


class ImportedGrant(models.Model):
    # ordering by creation date
    class Meta:
        ordering = ['-creation_date']

    # Title	Siebel	Name of the grant			PROJECT_TITLE
    title = models.CharField(max_length=1024, default='')
    # Grant Reference	Siebel	Unique identifier for the grant			GRANTREFERENCE
    grant_ref = models.CharField(max_length=50, default='', blank=True)
    # grant to imported grant relationship
    grant = models.ForeignKey(to=Grant, on_delete=models.PROTECT, null=True, blank=True)
    # date imported grant was created
    # creation_date = models.DateTimeField(auto_now_add=True)
    creation_date = models.DateField(editable=False)
    #Date modified
    #modified_date = models.DateTimeField(editable=False)
    # Grant Status	Siebel	Active/Closed			GRANT_STATUS
    grant_status = models.CharField(max_length=50, default="Active",
                                    choices=(("Active", "Active"), ("Closed", "Closed")))
    # AmountAwarded	Siebel	Amount in pounds stirling			AMOUNT
    amount_awarded = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    # Call	Siebel	E.g. Standard Grant DEC06			CALL
    # ignore call for now
    # call = models.CharField(max_length=1024, default='', blank=True)
    # Grant Type	Siebel	E.g. RM grants & fees			GRANT_TYPE
    # The xls file run by RTS also contains Abstract and Objectives I presume these are from the GRANT
    grant_type = models.CharField(max_length=1024, default='', blank=True)
    # Scheme	Siebel	E.g. Standard Grant			SCHEME
    scheme = models.CharField(max_length=1024, default='', blank=True)
    # Lead Grant (Yes / No)	Siebel	Y/N			LEAD_GRANT
    lead_grant = models.BooleanField(null=True, blank=True)
    # Parent Grant	Siebel	Cross reference record to a lead grant record if the grant is covered by an
    # overarching DMP			PARENT_GRANT
    parent_grant = models.ForeignKey(Grant, on_delete=models.PROTECT, null=True, blank=True, related_name='child_grant')
    # Grant Holder	Siebel	Principal investigator (title, first name, surname)			GRANT_HOLDER
    grant_holder = models.CharField(max_length=256, default='', blank=True)
    # Department	Siebel	e.g. School of Geography, Earth and Environmental Sciences			DEPARTMENT
    department = models.CharField(max_length=256, default='', blank=True)
    # Research Organisation	Siebel	E.g. University of Birmingham			RESEARCH_ORG
    research_org = models.CharField(max_length=256, default='', blank=True)
    # Address 1	Siebel				ADDRESS1
    address1 = models.CharField(max_length=256, default='', blank=True)
    # Address 2	Siebel				ADDRESS2
    address2 = models.CharField(max_length=256, default='', blank=True)
    # City	Siebel				CITY
    city = models.CharField(max_length=256, default='', blank=True)
    # Post Code	Siebel				POSTCODE
    post_code = models.CharField(max_length=256, default='', blank=True)
    # E-Mail	Siebel	Email address			EMAIL
    email = models.EmailField(null=True, blank=True)
    # Work Number	Siebel	Work telephone number			WORK_NUMBER
    work_number = models.CharField(max_length=256, null=True, blank=True, default='')
    # data contact name
    data_contact = models.CharField(max_length=256, null=True, blank=True)
    # Data Contact Email	Siebel	PI may not always be the contact for data related issues
    # (although responsible for ensuring delivery of the data)			MISSING
    data_contact_email = models.EmailField(null=True, blank=True)
    # Data Contact Phone	Siebel	PI may not always be the contact for data related issues
    # (although responsible for ensuring delivery of the data)			MISSING
    data_contact_phone = models.CharField(max_length=256, null=True, blank=True, default='')
    # Routing Classification	Siebel	E.g. Earth, Freshwater			ROUTING_CLASSIFICATION
    routing_classification = models.CharField(max_length=200, blank=True, null=True,
                                              choices=(("Marine", "Marine"),
                                                       ("Earth", "Earth"),
                                                       ("Atmospheric", "Atmospheric"),
                                                       ("Freshwater", "Freshwater"),
                                                       ("Terrestrial", "Terrestrial"),
                                                       ("Earth Observation", "Earth Observation"),
                                                       ))
    # Secondary Classifications	Siebel	E.g. Co-funded 40%; Cross-Research Council: 100%			MISSING
    secondary_classification = models.CharField(max_length=256, null=True, blank=True)
    # Science Area	Siebel	E.g. Earth: 70% Marine:30%			MISSING
    science_area = models.CharField(max_length=256, null=True, blank=True)
    # NCAS (Yes/No)	Siebel	Y/N			NCAS
    ncas = models.BooleanField(blank=True, null=True)
    # NCEO (yes/No)	Siebel	Y/N			NCEO
    nceo = models.BooleanField(blank=True, null=True)
    # Comments	Siebel	Currently not in use			MISSING
    comments = models.TextField(default='', blank=True)
    # # Original Proposed Start Date Siebel Date field set to the same as Proposed
    # # Start Date when record first added to the list	MISSING
    # original_proposed_start_date = models.DateField(null=True, blank=True)
    # # Original Proposed End Date	Siebel	Date field  set to the same as Proposed End Date when record first
    # # added to the list			MISSING
    # original_proposed_end_date = models.DateField(null=True, blank=True)
    # Proposed Start date	Siebel				PROPOSED_ST_DT
    proposed_start_date = models.DateField(null=True, blank=True)
    # Proposed End date	Siebel				PROPOSED_END_DT
    proposed_end_date = models.DateField(null=True, blank=True)
    # Actual Start Date	Siebel				ACTUAL_START_DATE
    actual_start_date = models.DateField(null=True, blank=True)
    # Actual End Date	Siebel				ACTUAL_END_DATE
    actual_end_date = models.DateField(null=True, blank=True)
    # End Date Changed?	Siebel				MISSING
    # end_date_changed = models.BooleanField(null=True, blank=True)
    # # Start Date Changed?	Siebel				MISSING
    # start_date_changed = models.BooleanField(null=True, blank=True)
    # Abstract	Siebel		Truncated
    abstract = models.TextField(default='', blank=True)
    # Objectives	Siebel		Truncated
    objectives = models.TextField(default='', blank=True)
    # ticket created
    ticket = models.BooleanField(null=True, blank=True) #, editable=False, verbose_name='Ticket created')



    # ordered by newest imported grant first

    # def compare(self, obj):
    #     # excluded_keys =  # tuple containing names of attributes to exclude
    #     return self._compare(self, obj) #, excluded_keys)

    # def get_previous(self):
    #     previous = self.get_previous_by_creation_date()
    #     if previous.exists():
    #         return self._compare(self, previous)
    #
    #
    # def _compare(self, obj1, obj2): #, excluded_keys):
    #     d1, d2 = obj1.__dict__, obj2.__dict__
    #     old, new = {}, {}
    #     for k, v in d1.items():
    #     #    if k in excluded_keys:
    #     #     continue
    #         try:
    #             if v != d2[k]:
    #                 old.update({k: v})
    #                 new.update({k: d2[k]})
    #         except KeyError:
    #             old.update({k: v})
    #
    #     return old, new

    def get_diff_fields(self):
        model_fields = [field.name for field in self._meta.get_fields()]
        #imported_grants = self.grant.importedgrant_set.all()
        date = self.creation_date
        passed = self.grant.importedgrant_set.filter(creation_date__lt=date).order_by('creation_date')
        if len(list(passed)) > 0:
            previous = list(passed)[-1]
            if previous:
                changed_fields = list(filter(
                    lambda field: getattr(previous, field, None) != getattr(self, field, None), model_fields))
                return changed_fields

    @property
    def get_science_area(self):
        science_area = self.science_area
        science_area = science_area.replace(':', '').replace('%', '').split(' ')
        science_areas = dict(science_area[i:i + 2] for i in range(0, len(science_area), 2))
        top_area = max(science_areas, key=science_areas.get)
        grant = Grant.objects.get(grant_ref=self.grant_ref)
        grant.science_area = top_area
        grant.save()
        return top_area

    def save(self, *args, **kwargs):
        # On save, update timestamps
        exists = Grant.objects.filter(grant_ref=self.grant_ref).exists()
        if not self.creation_date:
            self.creation_date = timezone.now()
        #self.modified_date = timezone.now()

        if exists:
            existing_grant = Grant.objects.get(grant_ref=self.grant_ref)
            self.grant = existing_grant
            existing_grant.updated_imported_grant = True
            existing_grant.save()
        else:
            new_grant = Grant.objects.create(grant_ref=self.grant_ref, claimed=False, updated_imported_grant=False)
            self.grant = new_grant
        return super(ImportedGrant, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.grant_ref}: {self.title[:50]}: [{self.grant_holder}]"


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a user with given email and password
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields)

        # Set the username to match the email
        user.username = self.normalize_email(email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.EmailField(max_length=255)
    data_centre = models.CharField(max_length=200, blank=True, null=True,
                                   choices=(("BODC", "BODC"),
                                            ("CEDA", "CEDA"),
                                            ("EIDC", "EIDC"),
                                            ("NGDC", "NGDC"),
                                            ("PDC", "PDC"),
                                            ("ADS", "ADS"),
                                            ))

    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'data_centre']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


"""
NGDC Grants Round Category	NGDC	NGDC internal category
NGDC Correspondence	NGDC	Linked to NGDC Correspondence Document Library (will show the number of emails/items for the particular grant)
NGDC DMP Documents	NGDC	Linked to NGDC DMP Document Library (will show the number of DMP items for the particular grant)
BGS contact	NGDC	Name of BGS/NGDC primary contact for this grant
Large data expected (in TB)	NGDC	Number in terabytes
Date large data expected	NGDC	Yes, No or Null
Detailed Accession Item ID	NGDC	Detailed accession number where applicable
NGDC Notes	NGDC
Metadata - citation_id	NGDC
DOI	NGDC
NGDC date to contact	NGDC	Date for next contact
Reason to contact	NGDC	Reason for next contact
"""
