from rest_framework import serializers
from django.contrib.auth import get_user_model
from news.models import Article
from news.define import APP_VALUE_STATUS_CHOICE
from django.utils.text import slugify

User = get_user_model()

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'name', 'author', 'slug', 'status', 'ordering', 'special', 'content', 'image', 'category', 'created', 'publish_date']
        read_only_fields = ['id', 'slug', 'created']
    
    def validate_author(self, value):
        """
        Validate author field to ensure it's a valid User instance.
        """
        if not isinstance(value, User):
            raise serializers.ValidationError("Author must be a valid User instance.")
        return value

    def validate(self, data):
        """
        Custom validation for the serializer.
        """
        name = data.get('name')
        slug = slugify(name)
        status = data.get('status')
        
        instance = self.instance

        # Check if a blog with this name already exists (excluding current instance)
        if instance and instance.name != name and Blog.objects.filter(name=name).exists():
            raise serializers.ValidationError("A blog with this name already exists.")

        # Check if a blog with this slug already exists (excluding current instance)
        if instance and instance.slug != slug and Blog.objects.filter(slug=slug).exists():
            raise serializers.ValidationError("A blog with this slug already exists.")

        # Check if status is valid
        if status not in [choice[0] for choice in APP_VALUE_STATUS_CHOICE]:
            raise serializers.ValidationError("Invalid status value.")

        return data

    def create(self, validated_data):
        """
        Create and return a new `Article` instance, given the validated data.
        """
        validated_data['slug'] = slugify(validated_data['name'])  # Generate slug from name
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Article` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slugify(validated_data.get('name', instance.name))  # Regenerate slug if name changes
        instance.author = validated_data.get('author', instance.author)
        instance.status = validated_data.get('status', instance.status)
        instance.ordering = validated_data.get('ordering', instance.ordering)
        instance.special = validated_data.get('special', instance.special)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.category = validated_data.get('category', instance.category)
        instance.publish_date = validated_data.get('publish_date', instance.publish_date)
        instance.save()
        return instance