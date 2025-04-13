from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from .models import User
from .models import Admin
from .models import Organizer
from django.core.exceptions import ValidationError
from .models import Event
from .models import Feedback
from .models import Transaction
from .models import Registration
from .models import Complaint
class UserSignupSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirmPassword', 'firstName', 'lastName', 'emailID', 'contactNo']

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("Passwords do not match.")
        if not data.get('emailID') and not data.get('contactNo'):
            raise serializers.ValidationError("Either emailID or contactNo is required.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        return User.objects.create(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    


# app2/serializers.py


class AdminLoginSerializer(serializers.Serializer):
    emailID = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class OrganizerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            organizer = Organizer.objects.get(username=username)
        except Organizer.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        if organizer.password != password:
            raise serializers.ValidationError("Invalid username or password.")

        return {
            "id": organizer.id,
            "username": organizer.username
        }
    
# app2/serializers.py

from rest_framework import serializers
from .models import Organizer

class OrganizerSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Organizer
        fields = ['username', 'password', 'confirm_password', 'firstName', 'lastName', 'emailID', 'contactNo']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if not data.get('emailID') and not data.get('contactNo'):
            raise serializers.ValidationError("Either emailID or contactNo must be provided.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # remove before saving
        return Organizer.objects.create(**validated_data)
    



class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

# serializers.py
from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'



class OrganizerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['id', 'username', 'firstName', 'lastName', 'emailID', 'contactNo', 'organization', 'verificationStatus']


#9
class OrganizerAvgRatingSerializer(serializers.Serializer):
    organizerID = serializers.IntegerField()
    firstName = serializers.CharField()
    lastName = serializers.CharField(allow_null=True)
    avgRating = serializers.FloatField()

#10
class ComplaintCountSerializer(serializers.Serializer):
    organizer_id = serializers.IntegerField()
    event_id = serializers.IntegerField(required=False)
    complaints = serializers.IntegerField()

#11
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id']  # Don't show user ID
#12
class AdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['id']  # Don't show admin ID
#13
class OrganizerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        exclude = ['id']  # Don't show organizer ID

#14
class UnverifiedOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

#15
class FeedbackSerializer(serializers.ModelSerializer):
    eventName = serializers.CharField(source='event.eventName', read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['eventName', 'Rating', 'Comments', 'Created_At']


#16
# serializers.py
class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['id']  # or use fields if you want specific ones
#17
class EventBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['eventName', 'startDate', 'startTime', 'endDate', 'endTime']

class UserRegistrationSerializer(serializers.ModelSerializer):
    event = EventBasicSerializer()
    transaction = TransactionDetailSerializer()

    class Meta:
        model = Registration
        fields = ['event', 'transaction']

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'firstName', 'lastName']

class EventBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'eventName', 'category', 'startDate', 'endDate']

#18
class ComplaintDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    event = EventBasicSerializer(read_only=True)

    class Meta:
        model = Complaint
        fields = '__all__'
#19
class FeedbackDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    event = EventBasicSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
#20
class TransactionDetailSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    event = EventBasicSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

#21
class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'firstName']

class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'eventName', 'category', 'startDate', 'endDate']

class TransactionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'method_of_payment', 'date_of_payment', 'status']

class RegistrationDetailSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)
    event = EventSummarySerializer(read_only=True)
    transaction = TransactionSummarySerializer(read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'transaction']