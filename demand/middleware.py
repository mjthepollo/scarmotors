from django.urls import reverse

from demand.sales_models import MockupCreated

USING_MOCKUP_LINKS = [
    "edit_register", "came_out_modal"
]

DEBUG_LINKS = ["history_sidebar"]

USING_MOCKUP_LINKS = USING_MOCKUP_LINKS + DEBUG_LINKS


def check_if_using_mockup(path_info):
    for link in USING_MOCKUP_LINKS:
        if link in path_info:
            return True
    return False


def remove_mockups(get_response):
    def middleware(request):
        if not check_if_using_mockup(request.path_info):
            if MockupCreated.objects.exists():
                for mockup_created in MockupCreated.objects.all():
                    mockup_created.remove_mockups()
                    print("REMOVE MOCKUPS!!!")
        response = get_response(request)
        return response
    return middleware
