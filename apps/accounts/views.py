from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import UserAccountCreationForm, SignInForm
from helpers.response.decorators import redirect_authenticated


@redirect_authenticated("dashboard", method="get")
class SignInView(generic.TemplateView):
    """View for user sign in"""

    template_name = "accounts/signin.html"
    form_class = SignInForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user_account = authenticate(request, username=email, password=password)

            if user_account:
                login(request, user_account)
                next_url = request.GET.get("next")
                return redirect(next_url or "dashboard")

            messages.error(request, "Invalid credentials, please try again")
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

        return redirect("accounts:signin")


@redirect_authenticated("dashboard", method="get")
class SignUpView(generic.CreateView):
    """View for user sign up"""

    form_class = UserAccountCreationForm
    template_name = "accounts/signup.html"
    success_url = "/accounts/sign-in/"

    def form_invalid(self, form: UserAccountCreationForm) -> HttpResponse:
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class SignOutView(LoginRequiredMixin, generic.View):
    """View for user sign out"""

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:signin")


user_signin_view = SignInView.as_view()
user_signout_view = SignOutView.as_view()
user_signup_view = SignUpView.as_view()
