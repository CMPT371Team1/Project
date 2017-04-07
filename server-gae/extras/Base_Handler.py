from google.appengine.ext.webapp import template
from webapp2_extras import auth
from webapp2_extras import sessions
import webapp2
import os


class BaseHandler(webapp2.RequestHandler):
    """
    contains business logic sign up and authentication users.
    Also contains some utility functions that are used by all handler class.
    """
    def options(self):
        """
        options: set up the headers from different controls over IP
        :return: nothing
        """
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = \
            'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = \
            'POST, GET, PUT, DELETE'

    @webapp2.cached_property
    def auth(self):
        """
        Shortcut to access the auth instance as a property
        :return: the auth instance of the property, which can be used to
        check the access measures of the property
        """
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """
        Shortcut to access a subset of the user attributes that are stored
        in the session.
        The list of attributes to store in the session is specified in
        config['webapp2_extras.auth']['user_attributes'].
        :returns A dictionary with most recent user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """
        Shortcut to access the current logged-in user. Unlike user_info, it
        fetches information from the persistence layer and
        returns an instance of the underlying model.
        :returns The instance of the user model associated to the signed-in
        user.
        """
        user = self.user_info
        return self.user_model.get_by_id(user['userId']) if user else None

    @webapp2.cached_property
    def user_model(self):
        """
        Return the implementation of the user model.
        It is consistent with config['webapp2_extras.auth']['user_model'],
        if set.
        :return the user model, in our case it will User
        """
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        """
        Shortcut to access the current session.
        :return  current session
        """
        return self.session_store.get_session(backend="datastore")

    def render_template(self, view_filename, params=None):
        """
        Get the template web page based on the file name
        :param view_filename: html file that needs to be displayed on browser.
        :param params: Any arguments required by the page if any.
        :return: Nothing
        """
        if not params:
            params = {}
        user = self.user_info
        params['user'] = user
        path = os.path.join(os.path.dirname(__file__), view_filename)
        self.response.out.write(template.render(path, params))

    def display_message(self, message):
        """
        Utility function to display a template with a simple message
        :param message: Message to be displayed on the web page
        :return:  Nothing
        """
        params = {
            'message': message
        }
        self.render_template('../webpages/Message.html', params)

    # this is needed for webapp2 sessions to work
    def dispatch(self):
        """
        Dispatch is required by each Handler to, actually work with webapp2
         This sets up the session storage and send request to dispatch handler.
        session.
        :return: Nothing
        """

        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions
            self.session_store.save_sessions(self.response)


class MainHandler(BaseHandler):
    """
    Main handler was basically created for browser testing.
    """
    def get(self):
        self.render_template('../webpages/Home.html')
