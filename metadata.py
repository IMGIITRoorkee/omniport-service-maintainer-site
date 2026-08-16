from rest_framework.metadata import SimpleMetadata


class PublicFieldMetadata(SimpleMetadata):
    """
    SimpleMetadata reports serializer fields only to callers allowed to write.
    The public team, alumni and profile pages read their role and designation
    labels out of that block, so it has to outlive the write routes
    """

    def determine_actions(self, request, view):
        """
        Return the serializer's field information under the write method this
        route advertised before it became read-only
        :param request: the request being processed
        :param view: the view processing the request
        :return: a map of one method name to serializer field information
        """

        method = 'PUT' if getattr(view, 'detail', False) else 'POST'
        return {method: self.get_serializer_info(view.get_serializer())}
