from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone


class Grant(models.Model):
    #title
    title = models.CharField(max_length=1024, default='')
    # Grant Reference	Siebel	Unique identifier for the grant			GRANTREFERENCE
    grant_ref = models.CharField(max_length=50, default='', blank=True)
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
                                             help_text="Datasets Delivered as per DMP?	Sharepoint	Yes, No or Null")
    # Sanctions Recommended	Sharepoint	Yes, No or Null
    sanctions_recommended = models.BooleanField(null=True, blank=True)
    # C for S found?	Sharepoint	Yes/No/Grant not found
    case_for_support_found = models.BooleanField(null=True, blank=True)
    #claim status
    claim_status = models.CharField(max_length=256, null=True, blank=True)
    # checks for updated imported grant (more than one version)
    updated_imported_grant = models.BooleanField(null=True, blank=True, editable=False, verbose_name='Grant updated')
    #programme - one programme can have many grants
    #programme = models.ForeignKey(to='dmp.Programme', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.grant_ref}: {self.title[:50]}"

class ImportedGrant(models.Model):
    #ordering by creation date
    class Meta:
      ordering = ['-creation_date']
    # Title	Siebel	Name of the grant			PROJECT_TITLE
    title = models.CharField(max_length=1024, default='')
    # Grant Reference	Siebel	Unique identifier for the grant			GRANTREFERENCE
    grant_ref = models.CharField(max_length=50, default='', blank=True)
    #grant to imported grant relationship
    grant = models.ForeignKey(to=Grant, on_delete=models.PROTECT, null=True, blank=True)
    #date imported grant was created
    #creation_date = models.DateTimeField(auto_now_add=True)
    creation_date = models.DateTimeField(editable=False)
    # Grant Status	Siebel	Active/Closed			GRANT_STATUS
    grant_status = models.CharField(max_length=50, default="Active",
                                    choices=(("Active", "Active"), ("Closed", "Closed")))
    # AmountAwarded	Siebel	Amount in pounds stirling			AMOUNT
    amount_awarded = models.IntegerField(null=True, blank=True)
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
    parent_grant = models.ForeignKey(on_delete=models.PROTECT, to='ImportedGrant', null=True, blank=True)
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
    ncas = models.CharField(max_length=200, blank=True, null=True,
                                              choices=(("Yes", "Yes"),
                                                       ("No", "No")))
    # NCEO (yes/No)	Siebel	Y/N			NCEO
    nceo = models.CharField(max_length=200, blank=True, null=True,
                                              choices=(("Yes", "Yes"),
                                                       ("No", "No")))
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
    # ordered by newest imported grant first

    def save(self, *args, **kwargs):
        #On save, update timestamps
        exists = Grant.objects.filter(grant_ref=self.grant_ref).exists()
        if not self.creation_date:
            self.creation_date = timezone.now()
        if exists:
            self.grant = Grant.objects.get(grant_ref=self.grant_ref)
        else:
            new_grant = Grant.objects.create(grant_ref=self.grant_ref, title=self.title, lead_grant=self.lead_grant)
            self.grant = new_grant
        return super(ImportedGrant, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.grant_ref}: {self.title[:50]}: [{self.grant_holder}]"

class MyUserManager(BaseUserManager):
    def create_user(self, email, data_centre, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            data_centre=data_centre,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, data_centre, first_name, last_name, password):
        user = self.create_user(
            email,
            password=password,
            data_centre=data_centre,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    data_centre = models.CharField(max_length=200, blank=True, null=True,
                                            choices=(("BODC", "BODC"),
                                                     ("CEDA", "CEDA"),
                                                     ("EIDC", "EIDC"),
                                                     ("NGDC", "NGDC"),
                                                     ("PDC", "PDC"),
                                                     ("ADS", "ADS"),
                                                     ))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'data_centre']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

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
