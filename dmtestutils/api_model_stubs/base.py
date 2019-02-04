import re


class BaseAPIModelStub:
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

    def _format_framework(self, slug, oldstyle=False):
        """Return a dictionary with correct keys for framework slug"""
        family, iteration = re.match(r"^(?P<family>[a-z-]*)(?:-(?P<iteration>\d+))?$", slug).groups()
        name = (
            {
                "g-cloud": "G-Cloud",
                "digital-outcomes-and-specialists": "Digital Outcomes and Specialists",
            }.get(family,
                  slug.replace("-", " ").title())
        )
        if iteration:
            name += " " + iteration

        framework = {
            "family": family,
            "slug": slug,
            "name": name,
        }
        if not oldstyle:
            return framework
        else:
            oldstyle_keys = {
                "frameworkFamily": "family",
                "frameworkSlug": "slug",
                "frameworkName": "name",
            }
            return {
                oldstyle_key: framework[newstyle_key]
                for oldstyle_key, newstyle_key in oldstyle_keys.items()
            }

    def _format_values(self, d):
        """Format all entries in a dictionary using values from response data"""
        return {
            k: v.format(**self.response_data) for k, v in d.items()
        }

    def response(self):
        return self.response_data

    def single_result_response(self):
        if self.resource_name:
            return {
                self.resource_name: self.response()
            }
        return self.response()
