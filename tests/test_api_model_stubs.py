# Minimal tests to make sure stub overrides work
from datetime import datetime as dt
import pytest
from dmtestutils.api_model_stubs import (
    AuditEventStub, BriefStub, FrameworkStub, FrameworkAgreementStub, LotStub, SupplierStub, SupplierFrameworkStub,
)
from dmtestutils.api_model_stubs.lot import dos_lots


class TestAuditEventStub:

    def test_audit_event_stub_defaults(self):
        assert AuditEventStub().response() == {
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

    def test_audit_event_stub_with_kwarg_options(self):
        audit_stub = AuditEventStub(acknowledged=True, include_user='Dave User').response()
        assert audit_stub["acknowledgedAt"] == "2018-12-11T01:02:03.000000Z"
        assert audit_stub["acknowledgedBy"] == "acknowledger@example.com"
        assert audit_stub["userName"] == "Dave User"


class TestBriefStub:

    def test_brief_stub_defaults(self):
        assert BriefStub().response() == {
            "id": 1234,
            "title": "I need a thing to do a thing",
            "frameworkSlug": "digital-outcomes-and-specialists",
            "frameworkStatus": "live",
            "frameworkName": "Digital Outcomes and Specialists",
            "frameworkFramework": "digital-outcomes-and-specialists",
            "framework": {
                "family": "digital-outcomes-and-specialists",
                "name": "Digital Outcomes and Specialists",
                "slug": "digital-outcomes-and-specialists",
                "status": "live"
            },
            "isACopy": False,
            "lotName": "Digital Specialists",
            "lotSlug": "digital-specialists",
            "status": "draft",
            "users": [{"active": True,
                       "role": "buyer",
                       "emailAddress": "buyer@email.com",
                       "id": 123,
                       "name": "Buyer User"}],
            "createdAt": "2016-03-29T10:11:12.000000Z",
            "updatedAt": "2016-03-29T10:11:13.000000Z",
            "links": {}
        }

    @pytest.mark.parametrize(
        ("kwarg", "key", "value"), (
            ("status", "status", "live"),
            ("lot_name", "lotName", "A Lot Slug"),
            ("lot_slug", "lotSlug", "a-lot-slug"),
            ("clarification_questions", "clarificationQuestions", [{"question": "Why?", "answer": "Because"}]),
        )
    )
    def test_returns_mapping_which_can_be_changed_using_kwargs(self, kwarg, key, value):
        assert BriefStub(**{kwarg: value}).response()[key] == value

    @pytest.mark.parametrize(
        ("kwarg", "key", "inner_key", "value"), (
            ("framework_slug", "frameworkSlug", "slug", "a-framework-slug"),
            ("framework_name", "frameworkName", "name", "A Framework Name"),
            ("framework_family", "frameworkFramework", "family", "a framework framework"),
            ("framework_status", "frameworkStatus", "status", "status"),
        )
    )
    def test_framework_kwarg_changes_framework_value_and_framework_dictionary(self, kwarg, key, inner_key, value):
        brief = BriefStub(**{kwarg: value}).single_result_response()
        assert brief["briefs"][key] == value
        assert brief["briefs"]["framework"][inner_key] == value

    def test_user_id_kwarg(self):
        assert BriefStub(user_id=234).response()["users"][0]["id"] == 234

    def test_brief_clarification_questions_closed(self):
        brief = BriefStub(status='live', clarification_questions_closed=True).response()
        assert brief["clarificationQuestionsAreClosed"] is True

    @pytest.mark.parametrize("status", (
        "live",
        "closed",
        "awarded",
        "unsuccessful",
        "withdrawn",
        "cancelled",
    ))
    def test_if_status_is_not_draft_brief_contains_milestone_dates(self, status):
        brief = BriefStub(status=status).single_result_response()
        assert "createdAt" in brief["briefs"]
        assert "updatedAt" in brief["briefs"]
        assert "publishedAt" in brief["briefs"]
        assert "applicationsClosedAt" in brief["briefs"]
        assert "clarificationQuestionsClosedAt" in brief["briefs"]
        assert "clarificationQuestionsPublishedBy" in brief["briefs"]

    def test_if_status_is_withdrawn_brief_contains_milestone_dates(self):
        brief = BriefStub(status="withdrawn").single_result_response()
        assert "withdrawnAt" in brief["briefs"]

    def test_if_status_is_unsuccessful_brief_contains_milestone_dates(self):
        brief = BriefStub(status="unsuccessful").single_result_response()
        assert "unsuccessfulAt" in brief["briefs"]

    def test_if_status_is_cancelled_brief_contains_milestone_dates(self):
        brief = BriefStub(status="cancelled").single_result_response()
        assert "cancelledAt" in brief["briefs"]


class TestFrameworkStub:

    def test_default_values(self):
        assert FrameworkStub().response() == {
            "id": 1,
            "name": "G-Cloud 10",
            "slug": "g-cloud-10",
            "framework": "g-cloud",
            "family": "g-cloud",
            "status": "open",
            "clarificationQuestionsOpen": True,
            "lots": [
                {
                    "id": 9,
                    "slug": "cloud-hosting",
                    "name": "Cloud hosting",
                    "allowsBrief": False,
                    "oneServiceLimit": False,
                    "unitSingular": 'service',
                    "unitPlural": 'services',
                },
                {
                    "id": 10,
                    "slug": "cloud-software",
                    "name": "Cloud software",
                    "allowsBrief": False,
                    "oneServiceLimit": False,
                    "unitSingular": 'service',
                    "unitPlural": 'services',
                },
                {
                    "id": 11,
                    "slug": "cloud-support",
                    "name": "Cloud support",
                    "allowsBrief": False,
                    "oneServiceLimit": False,
                    "unitSingular": 'service',
                    "unitPlural": 'services',
                }
            ],
            "allowDeclarationReuse": True,
            "frameworkAgreementDetails": {
                "variations": {}
            },
            "countersignerName": "Zachary X. Signer",
            "frameworkAgreementVersion": "RM1557x",
            "variations": {},
            'clarificationsCloseAtUTC': '2000-01-01T00:00:00.000000Z',
            'clarificationsPublishAtUTC': '2000-01-02T00:00:00.000000Z',
            'applicationsCloseAtUTC': '2000-01-03T00:00:00.000000Z',
            'intentionToAwardAtUTC': '2000-01-04T00:00:00.000000Z',
            'frameworkLiveAtUTC': '2000-01-05T00:00:00.000000Z',
            'frameworkExpiresAtUTC': '2000-01-06T00:00:00.000000Z',
            'hasDirectAward': True,
            'hasFurtherCompetition': False,
        }

    @pytest.mark.parametrize(
        ("kwarg", "key", "value"), (
            ("status", "status", "live"),
            ("name", "name", "My overridden name"),
            ("clarification_questions_open", "clarificationQuestionsOpen", False),
            ("has_direct_award", "hasDirectAward", False),
            ("has_further_competition", "hasFurtherCompetition", True),
        )
    )
    def test_returns_mapping_which_can_be_changed_using_kwargs(self, kwarg, key, value):
        assert key in FrameworkStub().response()
        assert FrameworkStub(**{kwarg: value}).response()[key] == value

    @pytest.mark.parametrize(
        ("slug", "family"), (
            ("my-fake-framework", "my-fake-framework"),
            ("digital-outcomes-and-specialists", "digital-outcomes-and-specialists"),
            ("digital-outcomes-and-specialists-2", "digital-outcomes-and-specialists"),
            ("g-cloud-10", "g-cloud"),
        )
    )
    def test_slug_kwarg_changes_framework_name_slug_family(self, slug, family):
        framework = FrameworkStub(slug=slug).response()

        assert framework["slug"] == slug
        assert framework["framework"] == family
        assert framework["family"] == family

    def test_dos_slug_kwarg_changes_all_related_framework_details(self):
        expected = FrameworkStub().response()
        expected.update({
            "name": "Digital Outcomes and Specialists",
            "slug": "digital-outcomes-and-specialists",
            "framework": "digital-outcomes-and-specialists",
            "family": "digital-outcomes-and-specialists",
            "lots": dos_lots(),
            "frameworkAgreementDetails": {"variations": {}},
            "hasDirectAward": False,
            "hasFurtherCompetition": True,
        })

        assert FrameworkStub(slug='digital-outcomes-and-specialists').response() == expected

    def test_lots_kwarg_changes_lots_and_framework_agreement_details(self):
        lots = [LotStub(slug='cloud-hosting').response(), LotStub(slug='cloud-support').response()]

        expected = FrameworkStub().response()
        expected["lots"] = lots
        expected["frameworkAgreementDetails"]["lotOrder"] = ["cloud-hosting", "cloud-support"]
        expected["frameworkAgreementDetails"]["lotDescriptions"] = {
            "cloud-hosting": "Lot 1: Cloud hosting",
            "cloud-support": "Lot 2: Cloud support",
        }

        assert FrameworkStub(lots=lots).response() == expected

    @pytest.mark.parametrize(
        ("kwarg", "datetime_obj", "key", "value"), (
            ("clarifications_close_at", dt(2011, 1, 1), "clarificationsCloseAtUTC", "2011-01-01T00:00:00.000000Z"),
            ("clarifications_publish_at", dt(2011, 2, 2), "clarificationsPublishAtUTC", "2011-02-02T00:00:00.000000Z"),
            ("applications_close_at", dt(2011, 3, 3), "applicationsCloseAtUTC", "2011-03-03T00:00:00.000000Z"),
            ("intention_to_award_at", dt(2011, 4, 4), "intentionToAwardAtUTC", "2011-04-04T00:00:00.000000Z"),
            ("framework_live_at", dt(2011, 5, 5), "frameworkLiveAtUTC", "2011-05-05T00:00:00.000000Z"),
            ("framework_expires_at", dt(2011, 6, 6), "frameworkExpiresAtUTC", "2011-06-06T00:00:00.000000Z"),
        )
    )
    def test_date_kwargs_can_be_datetime(self, kwarg, datetime_obj, key, value):
        assert key in FrameworkStub().response()
        assert FrameworkStub(**{kwarg: datetime_obj}).response()[key] == value
        assert kwarg not in FrameworkStub(**{kwarg: datetime_obj}).response()

    @pytest.mark.parametrize(
        ("kwarg", "key", "value"), (
            ("clarifications_close_at", "clarificationsCloseAtUTC", "2011-01-01T00:00:00.000000Z"),
            ("clarifications_publish_at", "clarificationsPublishAtUTC", "2011-02-02T00:00:00.000000Z"),
            ("applications_close_at", "applicationsCloseAtUTC", "2011-03-03T00:00:00.000000Z"),
            ("intention_to_award_at", "intentionToAwardAtUTC", "2011-04-04T00:00:00.000000Z"),
            ("framework_live_at", "frameworkLiveAtUTC", "2011-05-05T00:00:00.000000Z"),
            ("framework_expires_at", "frameworkExpiresAtUTC", "2011-06-06T00:00:00.000000Z"),
        )
    )
    def test_date_kwargs_can_be_string(self, kwarg, key, value):
        assert key in FrameworkStub().response()
        assert FrameworkStub(**{kwarg: value}).response()[key] == value
        assert kwarg not in FrameworkStub(**{kwarg: value}).response()

    def test_null_framework_agreement_version_is_allowed(self):
        assert FrameworkStub(framework_agreement_version=None).response()['frameworkAgreementVersion'] is None


class TestFrameworkAgreementStub:

    def test_framework_agreement_stub_default_values(self):
        assert FrameworkAgreementStub().response() == {
            'id': 1234,
            'supplierId': 43333,
            'frameworkSlug': "digital-outcomes-and-specialists-3",
            'status': ''
        }

    def test_framework_agreement_stub_with_optional_keys(self):
        assert FrameworkAgreementStub(
            signed_agreement_details={
                "frameworkAgreementVersion": "RM1557.10",
                "signerName": "A. Nonymous",
                "signerRole": "The Boss",
                "uploaderUserId": 46666
            },
            signed_agreement_path='/path/to/signed/agreement',
            signed_agreement_returned_at="2018-02-09T16:00:00.000000Z",
            countersigned_agreement_details={
                "approvedByUserId": 13333,
                "countersignerName": "Niall Quinn",
                "countersignerRole": "Category Director"
            },
            countersigned_agreement_returned_at="2018-05-09T16:00:00.000000Z",
            countersigned_agreement_path='/path/to/countersigned/agreement'
        ).response() == {
            'id': 1234,
            'supplierId': 43333,
            'frameworkSlug': "digital-outcomes-and-specialists-3",
            'status': '',
            'signedAgreementDetails': {
                "frameworkAgreementVersion": "RM1557.10",
                "signerName": "A. Nonymous",
                "signerRole": "The Boss",
                "uploaderUserId": 46666
            },
            'signedAgreementPath': '/path/to/signed/agreement',
            'signedAgreementReturnedAt': "2018-02-09T16:00:00.000000Z",
            'countersignedAgreementDetails': {
                "approvedByUserId": 13333,
                "countersignerName": "Niall Quinn",
                "countersignerRole": "Category Director"
            },
            'countersignedAgreementReturnedAt': "2018-05-09T16:00:00.000000Z",
            'countersignedAgreementPath': '/path/to/countersigned/agreement'
        }


class TestLotStub:

    def test_lot_stub_default_values(self):
        assert LotStub().response() == {
            "id": 1,
            "slug": "some-lot",
            "name": "Some lot",
            "allowsBrief": False,
            "oneServiceLimit": False,
            "unitSingular": "service",
            "unitPlural": "services",
        }

    @pytest.mark.parametrize(
        ("kwarg", "key", "value"), (
            ("slug", "slug", "my-special-lot"),
            ("allows_brief", "allowsBrief", True),
            ("one_service_limit", "oneServiceLimit", True),
            ("unit_singular", "unitSingular", "brief"),
            ("unit_plural", "unitPlural", "briefs"),
        )
    )
    def test_returns_mapping_which_can_be_changed_using_kwargs(self, kwarg, key, value):
        assert key in LotStub().response()
        assert LotStub(**{kwarg: value}).response()[key] == value


class TestSupplierStub:

    def test_supplier_stub_defaults(self):
        assert SupplierStub().response() == {
            "companiesHouseNumber": "12345678",
            "companyDetailsConfirmed": True,
            "contactInformation": [
                {
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
            ],
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

    def test_supplier_stub_with_extra_params(self):
        s = SupplierStub(
            id=123,
            contact_id=321,
            other_company_registration_number='4444',
            company_details_confirmed=False
        )
        resp = s.response()

        assert resp['id'] == 123
        assert resp['name'] == "My Little Company"
        assert resp['links'] == {
            'self': 'http://localhost:5000/suppliers/123'
        }
        assert resp['contactInformation'][0]['links'] == {
            'self': 'http://localhost:5000/suppliers/123/contact-information/321'
        }
        assert resp['contactInformation'][0]['id'] == 321
        assert resp['companyDetailsConfirmed'] is False
        assert resp['otherCompanyRegistrationNumber'] == '4444'
        assert resp.get('companiesHouseNumber') is None
        assert resp['registrationCountry'] == 'country:NZ'

    def test_supplier_stub_single_result_response_with_service_counts(self):
        s = SupplierStub()
        resp = s.single_result_response()
        assert resp['suppliers']['service_counts'] == {
            "G-Cloud 9": 109,
            "G-Cloud 8": 108,
            "G-Cloud 7": 107,
            "G-Cloud 6": 106,
            "G-Cloud 5": 105
        }


class TestSupplierFrameworkStub:

    def test_supplier_framework_stub_defaults(self):
        sf = SupplierFrameworkStub()
        assert sf.response() == {
            'agreedVariations': {},
            'agreementDetails': {},
            'agreementId': None,
            'agreementPath': None,
            'agreementReturnedAt': None,
            'agreementStatus': None,
            'applicationCompanyDetailsConfirmed': None,
            'countersigned': False,
            'countersignedAt': None,
            'countersignedDetails': None,
            'countersignedPath': None,
            'declaration': {},
            "frameworkFamily": "g-cloud",
            "frameworkFramework": "g-cloud",
            "frameworkSlug": "g-cloud-10",
            "onFramework": False,
            "prefillDeclarationFromFrameworkSlug": None,
            "supplierId": 886665,
            "supplierName": "Kev's Pies"
        }

    def test_supplier_framework_stub_with_options(self):
        sf = SupplierFrameworkStub(
            agreed_variations=True,
            supplier_id=1234,
            framework_slug='g-cloud-9',
            on_framework=True,
            prefill_declaration_from_slug='g-cloud-8',
            with_declaration=True,
            declaration_status='on-hold',
            with_agreement=True,
            with_users=True,
            application_company_details_confirmed=True,
        )
        assert sf.response() == {
            "agreedVariations": {
                "1": {
                    "agreedAt": "2018-05-04T16:58:52.362855Z",
                    "agreedUserEmail": "stub@example.com",
                    "agreedUserId": 123,
                    "agreedUserName": "Test user"
                }
            },
            "agreementDetails": {
                "frameworkAgreementVersion": "RM1557ix",
                "signerName": "A. Nonymous",
                "signerRole": "The Boss",
                "uploaderUserId": 443333,
                "uploaderUserName": "Test user",
                "uploaderUserEmail": "stub@example.com",
            },
            "agreementId": 9876,
            'agreementPath': 'not/the/real/path.pdf',
            "agreementReturned": True,
            'agreementReturnedAt': "2017-05-17T14:31:27.118905Z",
            'agreementStatus': "countersigned",
            'applicationCompanyDetailsConfirmed': True,
            'countersigned': True,
            'countersignedAt': "2017-06-15T08:41:46.390992Z",
            'countersignedDetails': {
                "approvedByUserId": 123,
                "approvedByUserEmail": "stub@example.com",
                "approvedByUserName": "Test user",
            },
            'countersignedPath': None,
            'declaration': {
                "nameOfOrganisation": "My Little Company",
                "organisationSize": "micro",
                "primaryContactEmail": "supplier@example.com",
                "status": 'on-hold',
            },
            "frameworkFamily": "g-cloud",
            "frameworkFramework": "g-cloud",
            "frameworkSlug": "g-cloud-9",
            "onFramework": True,
            "prefillDeclarationFromFrameworkSlug": "g-cloud-8",
            "supplierId": 1234,
            "supplierName": "Kev's Pies"
        }
