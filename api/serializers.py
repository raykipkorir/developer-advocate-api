from rest_framework import serializers
from .models import Advocate, Company

class CompanySerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Company
        fields = ["username", "name", "bio", "employee_count"]

    def get_employee_count(self, obj):
        count = obj.advocate_set.count()
        return count


class AdvocateSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Advocate
        fields = ["username", "name", "bio", "twitter_url", "profile_pic_url", "following_count", "followers_count", "company"]