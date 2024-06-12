from .resources import HelloWorld
from .resources import AddStaff

def register_routes(api):
    api.add_resource(HelloWorld, '/')

def ai_routes(api):
    api.add_resource(AddStaff, '/add/staff')
