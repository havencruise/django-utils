from django import template
from django.db.models.loading import get_model
from investments.models import 

register = template.Library()

def get_qs_for_model(val):
    ''' Usage:   get_qs_for_model('appname.modelname')
        Example: get_qs_for_model('library.Book') ''' 
    try:
        app_label, model_name = val.split(".") 
    except ValueError:
        # if we can't split, assume the model in investments
        app_label = ''
        model_name = val
    model = get_model(app_label, model_name)
    if model is None:
        raise template.TemplateSyntaxError('%s is not found' % val)
    return model.objects.all()


@register.tag(name="load_qs_for_model")
def load_model_objects(parser, token):
    '''  Example usage: {% load_qs_for_model library.Book as books %} '''
    
    tokens = token.contents.split()
    if len(tokens) != 4:
        raise template.TemplateSyntaxError("There must be 3 arguments given for %r " % tokens[0])
    if tokens[2] != 'as':
        raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
    
    qs = get_qs_for_model(tokens[1])

    return AppliedValueNode(qs, tokens[3])


class AppliedValueNode(template.Node):
    def __init__(self, val, var):
        self.val = val
        self.var = var

    def render(self, context):
        val = self.val
        var = self.var 
        context[var] = val
        return ''

