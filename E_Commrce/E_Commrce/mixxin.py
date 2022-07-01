from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {

            'message': 'Successfully',
            'data': data
        }

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
