"""
Generates example JSON responses for commonly-used serializable API models,
as given by the model's .serialize() method.

The default field values can be overridden on initialisation by providing **kwargs.

'resource_name' can be used to provide an additional single_result_response format,
with the resource_name as a top level key.

Some serializable models are not directly accessed by an API GET call, e.g. Lot, ContactInformation.
In these cases resource_name is set to None.

Example usage:

  from dmtestutils.api_model_stubs import BriefStub

  @mock.patch('dmapiclient.get_brief')
  def test_a_view_that_needs_briefs_from_the_api(mocked_get_brief_method):
     example_brief = BriefStub(framework_slug="digital-outcomes-and-specialists-3")
     mocked_get_brief_method.return_value = example_brief.single_result_response()

"""
from datetime import datetime as dt


class BaseAPIModelStub:

    resource_name = None
    default_data = {}
    optional_keys = []

    def __init__(self, **kwargs):
        self.response_data = self.default_data.copy()

        # Backwards compatibility for snake case kwargs
        for camelcase_key, snakecase_kwarg in self.optional_keys:
            if kwargs.get(snakecase_kwarg) is not None:
                self.response_data[camelcase_key] = kwargs.pop(snakecase_kwarg)

        self.response_data.update(**kwargs)

    def response(self):
        return self.response_data

    def single_result_response(self):
        if self.resource_name:
            return {
                self.resource_name: self.response()
            }
        return self.response()


class AuditEventStub(BaseAPIModelStub):
    resource_name = 'auditEvents'
    default_data = {
            'id': 123,
            'type': "update_brief_response",
            'acknowledged': False,
            'user': "supplier@example.com",
            'data': {
                "briefResponseData": {
                    "essentialRequirementsMet": True
                },
                "briefResponseId": 44444
            },
            'objectType': "BriefResponse",
            'objectId': 44444,
            'createdAt': "2018-12-10T01:02:03.000000Z",
            'links': {
                "self": "http://localhost/audit-events/123",
            }
    }
    optional_keys = [
        ('userName', 'include_user')
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get("acknowledged"):
            self.response_data["acknowledgedAt"] = "2018-12-11T01:02:03.000000Z"
            self.response_data["acknowledgedBy"] = "acknowledger@example.com"


class BriefStub(BaseAPIModelStub):
    resource_name = 'briefs'
    user = {
        "active": True,
        "role": "buyer",
        "emailAddress": "buyer@email.com",
        "id": 123,
        "name": "Buyer User"
    }
    default_data = {
        "id": 1234,
        "title": "I need a thing to do a thing",
        "frameworkSlug": "digital-outcomes-and-specialists",
        "frameworkName": "Digital Outcomes and Specialists",
        "frameworkFramework": "digital-outcomes-and-specialists",
        "frameworkStatus": "live",
        "framework": {
            "family": "digital-outcomes-and-specialists",
            "name": "Digital Outcomes and Specialists",
            "slug": "digital-outcomes-and-specialists",
            "status": "live",
        },
        "lotName": "Digital Specialists",
        "lotSlug": "digital-specialists",
        "isACopy": False,
        "status": "draft",
        "users": [user],
        "createdAt": "2016-03-29T10:11:12.000000Z",
        "updatedAt": "2016-03-29T10:11:13.000000Z",
        "links": {}
    }

    optional_keys = [
        ('lotName', 'lot_name'),
        ('lotSlug', 'lot_slug'),
        ('clarificationQuestions', 'clarification_questions'),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get('user_id'):
            self.user['id'] = kwargs.pop('user_id')
            self.response_data['users'] = [self.user]

        # Allow snake case framework_* kwargs for backwards compatibility
        for nested_framework_key, camelcase_key, snakecase_kwarg in [
            ('family', 'frameworkFramework', 'framework_family'),
            ('name', 'frameworkName', 'framework_name'),
            ('slug', 'frameworkSlug', 'framework_slug'),
            ('status', 'frameworkStatus', 'framework_status'),
        ]:
            if kwargs.get(snakecase_kwarg):
                # Update top level key
                self.response_data[camelcase_key] = kwargs.get(snakecase_kwarg)
                # Update nested key, deleting the snakecase kwarg which will have been updated already in super()
                self.response_data['framework'][nested_framework_key] = kwargs.get(snakecase_kwarg)
                del self.response_data[snakecase_kwarg]

        # Status-dependent values
        if self.response_data['status'] is not "draft":
            self.response_data["publishedAt"] = "2016-03-29T10:11:14.000000Z"
            self.response_data["applicationsClosedAt"] = "2016-04-07T00:00:00.000000Z"
            self.response_data["clarificationQuestionsClosedAt"] = "2016-04-02T00:00:00.000000Z"
            self.response_data["clarificationQuestionsPublishedBy"] = "2016-04-02T00:00:00.000000Z"
            if kwargs.get('clarification_questions_closed') is not None:
                self.response_data["clarificationQuestionsAreClosed"] = kwargs.pop('clarification_questions_closed')
                del self.response_data['clarification_questions_closed']

        if self.response_data['status'] is "withdrawn":
            self.response_data["withdrawnAt"] = "2016-05-07T00:00:00.000000Z"
        elif self.response_data['status'] is "unsuccessful":
            self.response_data["unsuccessfulAt"] = "2016-05-07T00:00:00.000000Z"
        elif self.response_data['status'] is "cancelled":
            self.response_data["cancelledAt"] = "2016-05-07T00:00:00.000000Z"


class BriefResponseStub(BaseAPIModelStub):
    resource_name = 'briefResponses'
    default_data = {

    }


class DirectAwardProjectStub(BaseAPIModelStub):
    resource_name = 'project'
    default_data = {

    }


class DirectAwardSearchStub(BaseAPIModelStub):
    resource_name = 'search'
    default_data = {

    }


class DraftServiceStub(BaseAPIModelStub):
    resource_name = 'services'
    default_data = {

    }


class FrameworkStub(BaseAPIModelStub):
    resource_name = 'frameworks'
    variations = {}
    framework_agreement_details = {
        "contractNoticeNumber": "2018/S 074-164715",
        "countersignerName": "Zachary X. Signer",
        "countersignerRole": "Category Director",
        "frameworkAgreementVersion": "RM1557.10",
        "frameworkExtensionLength": "12 months",
        "frameworkRefDate": "18-06-2018",
        "frameworkURL": "https://www.gov.uk/government/publications/g-cloud-7-framework-agreement",
        "lotDescriptions": {
            "cloud-hosting": "Lot 1: Cloud hosting",
            "cloud-software": "Lot 2: Cloud software",
            "cloud-support": "Lot 3: Cloud support"
        },
        "lotOrder": [
            "cloud-hosting",
            "cloud-software",
            "cloud-support"
        ],
        "pageTotal": 44,
        "signaturePageNumber": 3,
        "variations": {}
    }
    default_data = {
        "id": 1,
        "name": "G-Cloud 10",
        "slug": "g-cloud-10",
        "framework": "g-cloud",
        "family": "g-cloud",
        "status": "open",
        "clarificationQuestionsOpen": True,
        "allowDeclarationReuse": True,
        "frameworkAgreementDetails": {},
        "countersignerName": "Zachary X. Signer",
        "frameworkAgreementVersion": "RM1557x",
        "variations": {},
        'clarificationsCloseAtUTC': "2000-01-01T00:00:00.000000Z",
        'clarificationsPublishAtUTC': "2000-01-02T00:00:00.000000Z",
        'applicationsCloseAtUTC': "2000-01-03T00:00:00.000000Z",
        'intentionToAwardAtUTC': "2000-01-04T00:00:00.000000Z",
        'frameworkLiveAtUTC': "2000-01-05T00:00:00.000000Z",
        'frameworkExpiresAtUTC': "2000-01-06T00:00:00.000000Z",
    }
    optional_keys = [
        ('family', 'framework_family'),
        ('hasDirectAward', 'has_direct_award'),
        ('hasFurtherCompetition', 'has_further_competition'),
        ('clarificationQuestionsOpen', 'clarification_questions_open'),
        ('allowDeclarationReuse', 'allow_declaration_reuse')
    ]
    datestamp_keys = [
        ('clarificationsCloseAtUTC', 'clarifications_close_at'),
        ('clarificationsPublishAtUTC', 'clarifications_publish_at'),
        ('applicationsCloseAtUTC', 'applications_close_at'),
        ('intentionToAwardAtUTC', 'intention_to_award_at'),
        ('frameworkLiveAtUTC', 'framework_live_at'),
        ('frameworkExpiresAtUTC', 'framework_expires_at'),
    ]

    def derive_framework_details_from_slug(self, **kwargs):
        slug = kwargs.get('slug', 'g-cloud-10')
        name = kwargs.get('name')
        lots = kwargs.get('lots', [])

        if slug.startswith('g-cloud'):
            family = kwargs.get('framework_family') or kwargs.get('family') or 'g-cloud'
            name = name or 'G-Cloud {}'.format(slug.split('-')[-1])
            has_direct_award = kwargs.get('has_direct_award', True)
            has_further_competition = kwargs.get('has_further_competition', False)
            framework_iteration = int(slug.split('-')[-1])
            if not lots:
                lots = _as_a_service_lots() if framework_iteration <= 8 else _cloud_lots()

        elif slug.startswith('digital-outcomes-and-specialists'):
            family = kwargs.get('framework_family') or kwargs.get('family', 'digital-outcomes-and-specialists')
            name = name or slug.replace("-", " ").title().replace('And', 'and')
            has_direct_award = kwargs.get('has_direct_award', False)
            has_further_competition = kwargs.get('has_further_competition', True)
            if not lots:
                lots = _dos_lots()

        else:
            family = kwargs.get('framework_family') or kwargs.get('family', slug)
            name = name or slug.replace("-", " ").title()
            has_direct_award = kwargs.get('has_direct_award', True)
            has_further_competition = kwargs.get('has_further_competition', True)

        return {
            "name": name,
            "family": family,
            "hasDirectAward": has_direct_award,
            "hasFurtherCompetition": has_further_competition,
            "lots": lots
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Overwrite framework details and lots if slug supplied
        self.response_data.update(**self.derive_framework_details_from_slug(**kwargs))

        # Backwards compatibility for deprecated 'framework' key
        self.response_data['framework'] = self.response_data['family']

        # Allow framework_agreement_version kwarg with null value
        if 'framework_agreement_version' in kwargs:
            if kwargs.get('framework_agreement_version') is not None:
                self.response_data['frameworkAgreementVersion'] = kwargs.pop('framework_agreement_version')
                self.response_data['frameworkAgreementDetails']['frameworkAgreementVersion'] = \
                    self.response_data['frameworkAgreementVersion']
            else:
                # G7 frameworks and earlier have null versions
                self.response_data['frameworkAgreementVersion'] = None
                self.response_data['frameworkAgreementDetails']['frameworkAgreementVersion'] = None

        # Convert any datetime kwargs to datestamps
        for key, snakecase_kwarg in self.datestamp_keys:
            if kwargs.get(snakecase_kwarg) is not None:
                if isinstance(kwargs.get(snakecase_kwarg), dt):
                    self.response_data[key] = kwargs.get(snakecase_kwarg).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                else:
                    self.response_data[key] = kwargs.get(snakecase_kwarg)
                del self.response_data[snakecase_kwarg]

        # Copy variations to nested framework agreement details
        self.response_data['frameworkAgreementDetails']['variations'] = self.response_data['variations']


class FrameworkAgreementStub(BaseAPIModelStub):
    resource_name = 'agreement'
    default_data = {
        'id': 1234,
        'supplierId': 43333,
        'frameworkSlug': "digital-outcomes-and-specialists-3",
        'status': '',
    }
    optional_keys = [
        ('signedAgreementDetails', 'signed_agreement_details'),
        ('signedAgreementPath', 'signed_agreement_path'),
        ('signedAgreementReturnedAt', 'signed_agreement_returned_at'),
        ('countersignedAgreementDetails', 'countersigned_agreement_details'),
        ('countersignedAgreementReturnedAt', 'countersigned_agreement_returned_at'),
        ('countersignedAgreementPath', 'countersigned_agreement_path')
    ]


class OutcomeStub(BaseAPIModelStub):
    resource_name = 'outcome'
    default_data = {

    }


class LotStub(BaseAPIModelStub):
    default_data = {
        "id": 1,
        "slug": "some-lot",
        "name": "Some lot",
        "allowsBrief": False,
        "oneServiceLimit": False,
        "unitSingular": 'service',
        "unitPlural": 'services',
    }

    optional_keys = [
        ("allowsBrief", "allows_brief"),
        ("oneServiceLimit", "one_service_limit"),
        ("unitSingular", "unit_singular"),
        ("unitPlural", "unit_plural"),
        ("id", "lot_id")
    ]


class ServiceStub(BaseAPIModelStub):
    resource_name = 'services'
    default_data = {

    }


class SupplierStub(BaseAPIModelStub):
    resource_name = 'suppliers'
    contact_information = {
        "address1": "123 Fake Road",
        "city": "Madeupolis",
        "contactName": "Mr E Man",
        "email": "mre@company.com",
        "id": 4321,
        "links": {
            "self": "http://localhost:5000/suppliers/1234/contact-information/4321"
        },
        "phoneNumber": "01234123123",
        "postcode": "A11 1AA",
        "website": "https://www.mre.company"
    }
    default_data = {
        "companiesHouseNumber": "12345678",
        "companyDetailsConfirmed": True,
        "contactInformation": [contact_information],
        "description": "I'm a supplier.",
        "dunsNumber": "123456789",
        "id": 1234,
        "links": {
            "self": "http://localhost:5000/suppliers/1234"
        },
        "name": "My Little Company",
        "organisationSize": "micro",
        "registeredName": "My Little Registered Company",
        "registrationCountry": "country:GB",
        "tradingStatus": "limited company",
        "vatNumber": "111222333"
    }
    optional_keys = [
        ("otherCompanyRegistrationNumber", "other_company_registration_number"),
        ("companyDetailsConfirmed", "company_details_confirmed"),
    ]

    def single_result_response(self):
        # Include service_counts in API response only - this key isn't present in Supplier.serialize()
        self.response_data['service_counts'] = {
            "G-Cloud 9": 109,
            "G-Cloud 8": 108,
            "G-Cloud 7": 107,
            "G-Cloud 6": 106,
            "G-Cloud 5": 105
        }
        return {
            self.resource_name: self.response_data
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get('id'):
            self.response_data["links"]["self"] = "http://localhost:5000/suppliers/{id}".format(id=kwargs.get('id'))

        if kwargs.get('contact_id'):
            self.contact_information['id'] = kwargs.get('contact_id')
            self.contact_information['links']['self'] = \
                "http://localhost:5000/suppliers/{id}/contact-information/{contact_id}".format(
                    id=self.response_data['id'], contact_id=kwargs.get('contact_id')
                )
            self.response_data["contactInformation"] = [self.contact_information]
            # Don't include the kwarg in response
            del self.response_data['contact_id']

        if self.response_data.get('otherCompanyRegistrationNumber'):
            # We allow one or other of these registration numbers, but not both
            del self.response_data['companiesHouseNumber']
            # Companies without a Companies House number aren't necessarily overseas, but they might well be
            self.response_data['registrationCountry'] = 'country:NZ'


class SupplierFrameworkStub(BaseAPIModelStub):
    resource_name = 'frameworkInterest'
    default_data = {
        "agreedVariations": {},
        "agreementDetails": {},
        "agreementId": None,
        "agreementPath": None,
        "agreementReturnedAt": None,
        "agreementStatus": None,
        "applicationCompanyDetailsConfirmed": None,
        "countersigned": False,
        "countersignedAt": None,
        "countersignedDetails": None,
        "countersignedPath": None,
        "declaration": {},
        "frameworkFamily": "g-cloud",
        "frameworkFramework": "g-cloud",
        "frameworkSlug": "g-cloud-10",
        "onFramework": False,
        "prefillDeclarationFromFrameworkSlug": None,
        "supplierId": 886665,
        "supplierName": "Kev's Pies"
    }
    optional_keys = [
        ('supplierId', 'supplier_id'),
        ('frameworkSlug', 'framework_slug'),
        ('onFramework', 'on_framework'),
        ('prefillDeclarationFromFrameworkSlug', 'prefill_declaration_from_slug'),
        ('applicationCompanyDetailsConfirmed', 'application_company_details_confirmed')
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs.get('agreed_variations'):
            self.response_data['agreedVariations'].update({
                "1": {
                    "agreedAt": "2018-05-04T16:58:52.362855Z",
                    "agreedUserEmail": "stub@example.com",
                    "agreedUserId": 123,
                    "agreedUserName": "Test user"
                }
            })
        if kwargs.get('with_declaration'):
            self.response_data['declaration'] = {
                "nameOfOrganisation": "My Little Company",
                "organisationSize": "micro",
                "primaryContactEmail": "supplier@example.com",
                "status": kwargs.get('declaration_status', 'unstarted'),
            }
        if kwargs.get('with_agreement'):
            agreement_data = {
                "agreementId": 9876,
                "agreementReturned": True,
                "agreementReturnedAt": "2017-05-17T14:31:27.118905Z",
                "agreementDetails": {
                    "frameworkAgreementVersion": "RM1557ix",
                    "signerName": "A. Nonymous",
                    "signerRole": "The Boss",
                    "uploaderUserId": 443333,
                    "uploaderUserName": "Test user",
                    "uploaderUserEmail": "supplier@example.com",
                },
                "agreementPath": "not/the/real/path.pdf",
                "countersigned": True,
                "countersignedAt": "2017-06-15T08:41:46.390992Z",
                "countersignedDetails": {
                    "approvedByUserId": 123,
                },
                "agreementStatus": "countersigned",
            }
            if kwargs.get('with_users'):
                agreement_data['agreementDetails'].update({
                    "uploaderUserEmail": "stub@example.com",
                    "uploaderUserName": "Test user",
                })
                agreement_data['countersignedDetails'].update({
                    "approvedByUserEmail": "stub@example.com",
                    "approvedByUserName": "Test user",
                })
            self.response_data.update(agreement_data)

        for snakecase_key in [
            'agreed_variations', 'with_declaration', 'with_agreement', 'with_users', 'declaration_status'
        ]:
            if kwargs.get(snakecase_key):
                del self.response_data[snakecase_key]


class UserStub(BaseAPIModelStub):
    resource_name = 'users'
    default_data = {

    }


def _dos_lots():
    return [
        LotStub(
            lot_id=5, slug='digital-outcomes', name='Digital outcomes', allows_brief=True, one_service_limit=True
        ).response(),
        LotStub(
            lot_id=6, slug='digital-specialists', name='Digital specialists', allows_brief=True, one_service_limit=True
        ).response(),
        LotStub(
            lot_id=7, slug='user-research-studios', name='User research studios', unit_singular='lab',
            unit_plural='labs'
        ).response(),
        LotStub(
            lot_id=8, slug='user-research-participants', name='User research participants', allows_brief=True,
            one_service_limit=True
        ).response()
    ]


def _as_a_service_lots():
    return [
        LotStub(lot_id=1, slug='saas', name='Software as a Service').response(),
        LotStub(lot_id=2, slug='paas', name='Platform as a Service').response(),
        LotStub(lot_id=3, slug='iaas', name='Infrastructure as a Service').response(),
        LotStub(lot_id=4, slug='scs', name='Specialist Cloud Services').response()
    ]


def _cloud_lots():
    return [
        LotStub(lot_id=9, slug='cloud-hosting', name='Cloud hosting').response(),
        LotStub(lot_id=10, slug='cloud-software', name='Cloud software').response(),
        LotStub(lot_id=11, slug='cloud-support', name='Cloud support').response()
    ]
