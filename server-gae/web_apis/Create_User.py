from google.appengine.api import mail
from extras.Base_Handler import BaseHandler
from extras.Utils import *
from extras.Check_Invalid import *
from models.FacebookUser import FacebookUser
from extras.Required_Fields import check_required_valid
from API_NAME import create_user_api


class CreateUser(BaseHandler):
    """
    Creates a user after a person has successfully filled out the registration form.
    Post:
        @pre-cond: keys  valid key for email, firstName, lastName, password,
                         confirmedPassword, phone1, phone2(optional), city,
                         postalCode, and unique email.


        @post-cond: user  created and added to the Database
        @return-api: A dictionary with all the user details attached with
                     token, and userId is sent on valid request.
    """
    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(create_user_api, self.request.POST,
                                 self.response)

        if not valid:
            return

        if values['password'] != values['confirmedPassword']:
            error = {
                password_mismatch['error']:
                    'Password does not match confirmed password'}
            write_error_to_response(self.response, error,
                                    missing_invalid_parameter)

            return

        assert values['password'] == values['confirmedPassword']
        assert is_valid_password(values["password"])

        values['province'] = scale_province(str(values['province']))

        unique_properties = ["email"]
        user_data = self.user_model.create_user(
            values["email"], unique_properties, email=values["email"],
            first_name=values["firstName"],
            password_raw=values["password"], phone1=values["phone1"],
            phone2=values.get("phone2"),
            province=values["province"], city=values["city"],
            last_name=values.get("lastName"),
            verified=False)

        assert(user_data is not None)

        # user_data[0] contains True if user was created successfully
        if not user_data[0]:
            error_json = json.dumps({email_alreadyExists["error"]: "Email "
                                    "already exists"})
            self.response.write(error_json)
            self.response.set_status(missing_invalid_parameter)

            return

        # user_data[1] contains Token if user was created successfully

        assert user_data[1] is not None

        user = user_data[1]
        user_id = user.get_id()
        token = self.user_model.create_auth_token(user_id)

        # if user was created using a fbId then an entry needs to be mapped
        # from userId, and verification is not required if user is logged in
        # from face book.
        if "fbId" in values:
            fb_field = FacebookUser(user_id=int(user_id),
                                    fb_id=int(values["fbId"]))
            fb_field.put()
        else:
            signup_token = self.user_model.create_signup_token(user_id)

            # signing user in
            self.auth.get_user_by_token(user_id, token, remember=True,
                                        save_session=True)

            # sending email to verify user's email account.
            verification_url = self.uri_for(
                    "verification", type="v", user_id=user_id,
                    signup_token=signup_token, _full=True)
            message = mail.EmailMessage(
                sender="kasper@account.com",
                subject="Your account has been approved!")

            message.to = user.email
            message.body = """Thank you for creating an account!
             Please confirm your email address by clicking on the link below.
             {}
             """.format(verification_url)
            message.send()

        assert token is not None
        assert user_id is not None

        write_success_to_response(self.response, {"authToken": token,
                                                  "userId": user_id})
