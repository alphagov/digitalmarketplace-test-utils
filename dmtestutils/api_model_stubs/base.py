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

    def response(self):
        return self.response_data

    def single_result_response(self):
        if self.resource_name:
            return {
                self.resource_name: self.response()
            }
        return self.response()
