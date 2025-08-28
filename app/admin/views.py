from typing import ClassVar
from starlette_admin.contrib.sqla import ModelView

class UserAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "email",
        "username",
        "is_active",
        "is_admin",
        "created_at",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = ["created_at"]
    exclude_fields_from_create: ClassVar[list[str]] = ["created_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["created_at"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "email",
        "username",
        "is_active",
        "created_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class EventAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id", "title", "description",
        "start_datetime", "end_datetime",
        "location_url", "max_participant", "is_active", "created_at",
    ]
    exclude_fields_from_list: ClassVar[list[str]] = ["created_at", ]
    exclude_fields_from_create: ClassVar[list[str]] = ["created_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["created_at"]
    export_fields: ClassVar[list[str]] = [
        "id", "title", "description",
        "start_datetime", "end_datetime",
        "location_url", "max_participant", "is_active",
        "created_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class EventRegistrationAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "user",
        "event",
        "registered_at",
        "status"
    ]
    exclude_fields_from_list: ClassVar[list[str]] = ["registered_at"]
    exclude_fields_from_create: ClassVar[list[str]] = ["registered_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["registered_at"]
    export_fields: ClassVar[list[str]] = [
        "id",
        "user_id",
        "event_id",
        "registered_at",
        "status",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]