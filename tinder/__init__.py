from tinder.views import LoginFormView


def __init__(self, *args, **kwargs):
        super(LoginFormView, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-signin'

#default_app_config = 'tinder.tinder.MytinderAppConfig'

