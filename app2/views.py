from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from .models import User, Admin, Organizer,Event, Feedback, Complaint, Registration, Transaction
from .serializers import ComplaintCountSerializer, UserDetailSerializer, AdminDetailSerializer, OrganizerDetailSerializer, UnverifiedOrganizerSerializer, FeedbackSerializer
from .serializers import UserSignupSerializer, UserLoginSerializer, AdminLoginSerializer, OrganizerLoginSerializer, EventDetailSerializer, EventSerializer, OrganizerAvgRatingSerializer
from django.db.models import Q, F, Avg
from django.utils import timezone
from django.utils.timezone import now
from rest_framework.generics import ListAPIView
from .serializers import UnverifiedOrganizerSerializer
from django.shortcuts import get_object_or_404
from .serializers import UserRegistrationSerializer
from .serializers import EventBasicSerializer
from datetime import datetime
from .serializers import ComplaintDetailSerializer, FeedbackDetailSerializer, TransactionDetailSerializer
from .serializers import RegistrationDetailSerializer

class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "uid": user.id,
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    return Response({
                        "uid": user.id,
                        "username": user.username
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['emailID']
            password = serializer.validated_data['password']

            try:
                admin = Admin.objects.get(emailID=email)
                if admin.password == password:
                    return Response({
                        "id": admin.id,
                        "emailID": admin.emailID,
                        "role": admin.role
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

            except Admin.DoesNotExist:
                return Response({"error": "Admin not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# app2/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrganizerLoginSerializer

class OrganizerLoginView(APIView):
    def post(self, request):
        serializer = OrganizerLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# app2/views.py

from .serializers import OrganizerSignupSerializer

class OrganizerSignupView(APIView):
    def post(self, request):
        serializer = OrganizerSignupSerializer(data=request.data)
        if serializer.is_valid():
            organizer = serializer.save()
            return Response({
                "id": organizer.id,
                "username": organizer.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class EventDetailView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventDetailSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class FilteredEventView(APIView):
    def get(self, request):
        current_datetime = now().astimezone()
        current_date = current_datetime.date()
        current_time = current_datetime.time()

        # Mapping of shortform to matching category strings
        category_map = {
            'ea': ['Concert', 'Dance', 'Art'],
            'bt': ['Business', 'Tech'],
            'fl': ['Food', 'Expo'],
            'si': ['Charity'],
            'sf': ['Sports', 'Gaming']
        }

        # Get and normalize the filter param to lowercase
        filter_key = request.query_params.get('filter', '').lower()
        categories = category_map.get(filter_key, None)

        # Base query: upcoming events that are not full
        query = Event.objects.filter(
            Q(startDate__gt=current_date) |
            Q(startDate=current_date, startTime__gt=current_time)
        ).exclude(
            ticketsSold=F('maxAttendees')
        )

        # If a valid filter is provided, filter by category
        if categories:
            query = query.filter(category__in=categories)

        serializer = EventSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class EventsByOrganizerView(APIView):
    def get(self, request, organizer_id):
        current_datetime = now().astimezone()
        current_date = current_datetime.date()
        current_time = current_datetime.time()

        # Base query
        events = Event.objects.filter(organizer__id=organizer_id)

        # Optional filter: 0 = upcoming, 1 = past
        filter_value = request.query_params.get('filter', None)

        if filter_value == '0':
            # Upcoming: date is in future or today with time > now
            events = events.filter(
                Q(startDate__gt=current_date) |
                Q(startDate=current_date, startTime__gt=current_time)
            )
        elif filter_value == '1':
            # Past: date is in past or today with time < now
            events = events.filter(
                Q(startDate__lt=current_date) |
                Q(startDate=current_date, startTime__lt=current_time)
            )

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



# app2/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organizer
from .serializers import OrganizerListSerializer

class OrganizersByAdminView(APIView):
    def get(self, request, staff_id):
        organizers = Organizer.objects.filter(staff__id=staff_id)
        
        if not organizers.exists():
            return Response({"message": "No organizers found for this admin."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrganizerListSerializer(organizers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#(9)
class OrganizerAverageRatingView(APIView):
    def get(self, request, organizer_id):
        organizer = Organizer.objects.filter(id=organizer_id).first()

        if not organizer:
            return Response({"error": "Organizer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all event IDs organized by this organizer
        events = Event.objects.filter(organizer_id=organizer_id).values_list('id', flat=True)

        # Calculate average rating from Feedback linked to these events
        avg_rating = Feedback.objects.filter(event_id__in=events).aggregate(avg=Avg('Rating'))['avg']

        serializer = OrganizerAvgRatingSerializer({
            'organizerID': organizer.id,
            'firstName': organizer.firstName,
            'lastName': organizer.lastName,
            'avgRating': round(avg_rating, 2) if avg_rating is not None else 0.0
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
    

#(10)
class ComplaintCountView(APIView):
    def get(self, request, organizer_id):
        event_id = request.query_params.get('event_id', None)

        if event_id:
            complaints = Complaint.objects.filter(event__id=event_id, event__organizer__id=organizer_id)
            count = complaints.count()
            data = {
                'organizer_id': organizer_id,
                'event_id': int(event_id),
                'complaints': count
            }
        else:
            complaints = Complaint.objects.filter(event__organizer__id=organizer_id)
            count = complaints.count()
            data = {
                'organizer_id': organizer_id,
                'complaints': count
            }

        serializer = ComplaintCountSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#11
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'

#12
class AdminDetailView(RetrieveAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminDetailSerializer
    lookup_field = 'id'

#13
class OrganizerDetailView(RetrieveAPIView):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerDetailSerializer
    lookup_field = 'id'


#14
class UnverifiedOrganizerListView(ListAPIView):
    queryset = Organizer.objects.filter(verificationStatus=False)
    serializer_class = UnverifiedOrganizerSerializer

   

#15
class OrganizerEventFeedbackView(APIView):
    def get(self, request, organizer_id):
        event_id = request.query_params.get('event_id')

        if event_id:
            # Feedback for specific event
            event = get_object_or_404(Event, id=event_id, organizer__id=organizer_id)
            feedbacks = Feedback.objects.filter(event=event)
        else:
            # Feedback for all events by organizer
            events = Event.objects.filter(organizer__id=organizer_id)
            feedbacks = Feedback.objects.filter(event__in=events)
        
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#16
class UserRegistrationTransactionView(APIView):
    def get(self, request, user_id):
        registrations = Registration.objects.filter(user__id=user_id)
        serializer = UserRegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#17
class UserEventListView(APIView):
    def get(self, request, user_id):
        filter_type = request.query_params.get('filter')  # "1" or "2"
        now = datetime.now().date()

        event_ids = Registration.objects.filter(user__id=user_id, event__isnull=False).values_list('event__id', flat=True)
        events = Event.objects.filter(id__in=event_ids)

        if filter_type == '1':
            events = events.filter(startDate__gte=now)
        elif filter_type == '2':
            events = events.filter(endDate__lt=now)

        serializer = EventBasicSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#18
class ComplaintDetailView(APIView):
    def get(self, request, complaint_id):
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            serializer = ComplaintDetailSerializer(complaint)
            return Response(serializer.data)
        except Complaint.DoesNotExist:
            return Response({'error': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
        
#19
class FeedbackDetailView(APIView):
    def get(self, request, feedback_id):
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            serializer = FeedbackDetailSerializer(feedback)
            return Response(serializer.data)
        except Feedback.DoesNotExist:
            return Response({'error': 'Feedback not found'}, status=status.HTTP_404_NOT_FOUND)
        
#20
class TransactionDetailView(APIView):
    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            serializer = TransactionDetailSerializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        


class RegistrationDetailView(APIView):
    def get(self, request, registration_id):
        try:
            registration = Registration.objects.get(id=registration_id)
            serializer = RegistrationDetailSerializer(registration)
            return Response(serializer.data)
        except Registration.DoesNotExist:
            return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)