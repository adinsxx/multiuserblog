from base_handler import BaseHandler
from models import User
import re


class RegisterHandler(BaseHandler):

    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

    def get(self):
        self.render("auth/register.html")

    def post(self):
        user_name = self.request.get("username")
        user_password = self.request.get("password")
        password_verify = self.request.get("password_verify")
        user_email = self.request.get("email")

        param_list = dict(user_name=user_name, user_emai=user_email)
        any_error = False

        name_error = ""
        if user_name is None or not self.valid_username(user_name):
            param_list['name_error'] = "Invalid Username"
            any_error = True

        password_error = ""
        if not self.valid_password(user_password):
            param_list['password_error'] = "Invalid Password"
            any_error = True

        password_verify = ""
        if user_password != password_verify:
            param_list['password_repear_error'] = "Password do not match"
            any_erro = True

        email_erorr = ""
        if user_email is None or not self.valid_email(user_email):
            param_list['email_error'] = "Email invalid"
            any_error = True


        if not any_error:
            if User.by_name(user_name):
                self.render("auth/register.html",
                            name_error="User already exists")
            else:
                u = User.register(user_name, user_password, user_email)
                self.login(u)
                self.redirect("/welcome")
        else:
            self.render("auth/register.html", **param_list)

    def valid_username(self, username):
        return self.USER_RE.match(username)

    def valid_password(self, password):
        return self.PASS_RE.match(password)

    def valid_email(self, email):
        return self.MAIL_RE.match(email)


class LoginHandler(BaseHandler):

    def get(self):
        self.render("auth/login.html")

    def post(self):
        user_name = self.request.get("name")
        user_password = self.request.get("password")
        any_error = False
        param_list = dict(user_name=username)

        if not user_name:
            param_list['name_error'] = "Missing Username"
            any_error = True
        if not user_password:
            param_list['password_error'] = "Missing Password"
            any_error = True

        if any_error:
            self.render("auth/login.html", **param_list)
        else:
            u = User.login(user_name, user_password)
            if not u:
                param_list['login_error'] = "Invalid Username or Password"
                self.render("auth/login.html", **param_list)
            else:
                self.login(u)
                self.redirect("/welcome")


class LogoutHandler(BaseHandler):

    def get(self):
        self.logout()
        self.redirect('/login')


class WelcomeHandler(BaseHandler):

    def get(self):
        if self.user:
            self.render("auth/welcome.html")
        else:
            self.redirect("/login")
        
