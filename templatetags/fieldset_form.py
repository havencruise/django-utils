from django import template

register = template.Library()


@register.filter('get_form_field')
def get_form_field(form, field):
    return form[field]


@register.inclusion_tag('form_as_fieldset.html')
def form_as_fieldset_fields(form, fieldsets=None):
    """
    Render the form as a fieldset form.
    Example usage in template with 'myform' and 'myfieldsets as context attributes:
        {% form_as_fieldset_fields myform myfieldsets %}
    Sample fieldset:
    MY_FIELDSETS = (
        (
            'info',
            ('first_name', 'middle_name', 'last_name', 'is_published')
        ),
        (
            'image',
            ('profile_image', 'avatar_image', 'profile_image_crop')
        ),
        (
            'profile',
            ('title', 'location', 'profile_full', 'profile_brief',
            'website_url', 'average_artwork_cost', 'born_year',
            'deceased_year')
        ),
        (
            'focus area',
            ('styles', 'mediums')
        )
    )
    """
    if not fieldsets:
        fieldsets = (
            (
                '',
                tuple(form.fields.keys()),
            ),
        )
    return {'form': form, 'fieldsets' : fieldsets}


@register.filter('field_type')
def field_type(field):
    """
    Get the name of the field class.
    """
    if hasattr(field, 'field'):
        field = field.field
    s = (type(field.widget).__name__).replace('Input', '').lower()
    return s


@register.filter('strongify')
def strongify(name):
    """
    Takes a string and returns formatted strong version as in the example:
        Input: "My name is"
        Output: "My <strong> name is </strong>"

    """
    names = name.split(' ')
    if names[1:]:
        strong_string = "<strong>" + " ".join(names[1:]) + "</strong>"
        return names[0] +" " + strong_string
    else:
        return name