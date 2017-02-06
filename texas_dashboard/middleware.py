from texas_dashboard.utils import create_session_user_link


class SessionLinkingMiddleware(object):
    def process_view(self, request, *args, **kwargs):
        if request.user.id and request.session.session_key:
            user_id = int(request.user.id)
            session_key = request.session.session_key
            create_session_user_link(session_key, user_id)

