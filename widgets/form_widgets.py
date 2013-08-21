import json
from django import forms
from django.utils.html import escape
from django.utils.safestring import mark_safe


class AdminFileWidget(forms.FileInput):
    """
    A FileField Widget that shows its current value if it has one.
    """
    def __init__(self, attrs={}):
        super(AdminFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('<span class=\'current %s\'><a target="_blank" href="%s">%s </a> </span> ' \
                % (name, escape(value.url), 'View Current'))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class TextInputCustomMessageWidget(forms.TextInput):
    """
        A widget that appends a custom message to a text input
    """
    def __init__(self, attrs = None, **kwargs):
        self.__message__ = kwargs.pop('message', None)
        super(TextInputCustomMessageWidget, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        output = []
        output.append(super(TextInputCustomMessageWidget, self).render(name, value, attrs))
        if self.__message__:
            output.append('<span class="%s message">%s</span>' % (name, self.__message__))

        return mark_safe(u''.join(output))


class ReadOnlyFieldWidget(forms.HiddenInput):
    """
        A Widget that shows its current value if it has one as readonly.
    """
    def __init__(self, attrs={}):
        super(ReadOnlyFieldWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = """function updateDateTime(e){
            var el = document.getElementById(e)
        }
        """
        if type(value) is datetime.datetime:
            value = value.strftime('%a, %b %d %Y - %I:%M:%S %p')
        elif type(value) is datetime.date:
            value = value.strftime('%a, %b %d %Y')
        
        output = super(ReadOnlyFieldWidget, self).render(name, value, attrs)
        output += "%s" % value

        return mark_safe(output)


class jQMultiSelectWidget(forms.SelectMultiple):
    """
        A widget that uses jQuery UI MultiSelect on a ModelMultipleChoiceField.
    """
    def render(self, name, value, attrs=None, **kwargs):
        
        extra_options = None
        if kwargs.get('widget_options', None):
            extra_options = kwargs.pop('options')

        output = super(jQMultiSelectWidget, self).render(name, value, attrs)

        if attrs and 'id' in attrs:
            if extra_options:
                output = output + '''
                    <script type="text/javascript">$(function(){
                        $('#%s').multiselect(%s);
                    });</script>
                ''' % (attrs['id'], json.dumps(extra_options))
            else:
                output = output + '''
                    <script type="text/javascript">$(function(){
                        $('#%s').multiselect({});
                    });</script>
                ''' % attrs['id']
        elif name:
            if extra_options:
                output = output + '''
                    <script type="text/javascript">$(function(){
                        $('select[name=%s]').multiselect(%s);
                    });</script>
                ''' % (name, json.dumps(extra_options))
            else:
                output = output + '''
                    <script type="text/javascript">$(function(){
                        $('select[name=%s]').multiselect({});
                    });</script>
                ''' % name

        return mark_safe(output)


class jQDatepickerWidget(forms.DateInput):
    def render(self, name, value, attrs=None, **kwargs):
        extra_options = None
        if kwargs.get('widget_options', None):
            extra_options = kwargs.pop('widget_options')

        output = super(jQDatepickerWidget, self).render(name, value, attrs)

        if attrs and 'id' in attrs:
            if extra_options:
                output = output + '''
                    <script type="text/javascript">$(function(){
                        $.datepicker ? $('#%s').datepicker(%s) : false
                    });</script>
                ''' % (attrs['id'], json.dumps(extra_options))
            else:
                output = output + '''
                    <script type="text/javascript">$(function(){
                        $.datepicker ? $('#%s').datepicker({})  : false
                    });</script>
                ''' % attrs['id']

        return mark_safe(output)



