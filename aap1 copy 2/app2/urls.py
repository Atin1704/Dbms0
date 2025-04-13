from django.urls import path
from .views import SignupView, LoginView, AdminLoginView, OrganizerLoginView, OrganizerSignupView, EventDetailView, FilteredEventView, EventsByOrganizerView, OrganizersByAdminView
from .views import OrganizerAverageRatingView
from .views import ComplaintCountView
from .views import UserDetailView, AdminDetailView, OrganizerDetailView
from .views import UnverifiedOrganizerListView, OrganizerEventFeedbackView
from .views import UserRegistrationTransactionView
from .views import UserEventListView
from .views import ComplaintDetailView, FeedbackDetailView, TransactionDetailView
from .views import RegistrationDetailView
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('organizer/login/', OrganizerLoginView.as_view(), name='organizer-login'),
    path('organizer/signup/', OrganizerSignupView.as_view(), name='organizer-signup'),
    path('event/<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('events/filtered/', FilteredEventView.as_view(), name='filtered-events'),
    path('events/organizer/<int:organizer_id>/', EventsByOrganizerView.as_view(), name='events-by-organizer'),
    path('organizers/admin/<int:staff_id>/', OrganizersByAdminView.as_view(), name='organizers-by-admin'),
    path('organizer/<int:organizer_id>/average-rating/', OrganizerAverageRatingView.as_view(), name='organizer-average-rating'), #(9)
    path('organizer/<int:organizer_id>/complaints/', ComplaintCountView.as_view(), name='organizer-complaints'),  #(10)
    path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'),#11
    path('admin/<int:id>/', AdminDetailView.as_view(), name='admin-detail'),#12
    path('organizer/<int:id>/', OrganizerDetailView.as_view(), name='organizer-detail'),#13
    path('admin/unverified-organizers/', UnverifiedOrganizerListView.as_view(), name='unverified-organizers'),#14
    path('organizer/<int:organizer_id>/feedbacks/', OrganizerEventFeedbackView.as_view(), name='organizer-feedbacks'),#15
    path('user/<int:user_id>/registrations/', UserRegistrationTransactionView.as_view(), name='user-registrations'),#16
    path('user/<int:user_id>/events/', UserEventListView.as_view(), name='user-events'),#17
    path('complaint/<int:complaint_id>/', ComplaintDetailView.as_view(), name='complaint-detail'),#18
    path('feedback/<int:feedback_id>/', FeedbackDetailView.as_view(), name='feedback-detail'),#19   
    path('transaction/<int:transaction_id>/', TransactionDetailView.as_view(), name='transaction-detail'),#20   
    path('api/registration/<int:registration_id>/', RegistrationDetailView.as_view(), name='registration-detail'),#21




]








