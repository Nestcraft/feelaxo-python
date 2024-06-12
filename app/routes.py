from .resources import HelloWorld
from .resources import AddStaff
from .resources import VerifyStaff


def ai_routes(api):
    api.add_resource(AddStaff, '/add/staff')
    api.add_resource(VerifyStaff, '/verify/staff')
