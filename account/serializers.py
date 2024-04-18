from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    # add some validation
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password") # removing the password out of data
        user = super().create(validated_data) # create the user
        user.set_password(password) # hashing the password and add it in
        user.save()
        return user

"""
Nested Serializers
"""
class CurrentUserArticlesRelatedLinksSerializer(serializers.ModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name="news_article_retrieve_update_destroy_id", queryset=User.objects.all()
    )
    class Meta:
        model = User
        fields = ["id", "username", "email", "articles"]

class CurrentUserArticlesStringsSerializer(serializers.ModelSerializer):
    articles = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "articles"]
