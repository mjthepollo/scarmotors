from django.urls import reverse

from demand.sales_models import MockupCreated


def remove_mockups(get_response):

    def middleware(request):
        if not "edit_register" in request.path_info:
            if MockupCreated.objects.exists():
                for mockup_created in MockupCreated.objects.all():
                    mockup_created.remove_mockups()
                    print("REMOVE MOCKUPS!!!")
        response = get_response(request)
        return response

    return middleware
