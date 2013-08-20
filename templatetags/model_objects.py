from django import template
from django.db.models.loading import get_model

register = template.Library()

@register.tag(name="load_model")
def load_model_objects(parser, token):
    tokens = token.contents.split()
    if len(tokens) != 4:
        raise template.TemplateSyntaxError("There must be 3 arguments given for %r " % tokens[0])

    if tokens[2] != 'as':
        raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])

    return ModelNode(tokens[1], tokens[3])


class ModelNode(template.Node):
    def __init__(self, val, var):
        self.val = val
        self.var = var

    def render(self, context):
        val = self.val
        try:
            app_label, model_name = val.split(".") 
        except ValueError:
            # if we can't split, assume blank model 
            app_label = ''
            model_name = val

        model = get_model(app_label, model_name)

        if model is None:
            raise template.TemplateSyntaxError('%s is not found' % val)

        var = self.var 
        context[var] = model.objects.all()
        
        return ''
