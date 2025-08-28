from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models.models import User, Event, EventRegistration
from app.admin.auth import JSONAuthProvider
from app.admin.views import UserAdminView, EventAdminView, EventRegistrationAdminView

admin = Admin(
    engine=engine, title="Event System Admin", base_url="/admin", auth_provider=JSONAuthProvider(login_path="/login", logout_path="/logout"))

admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(EventAdminView(Event, icon="fa fa-event"))
admin.add_view(EventRegistrationAdminView(EventRegistration, icon="fa fa-tag"))
