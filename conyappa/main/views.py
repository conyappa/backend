from django.contrib.admin import site as admin_site

admin_site.site_header = "Con Yappa"
admin_site.site_title = "Con Yappa"


def trigger_error(_request):
    raise Exception("This is just a test.")
