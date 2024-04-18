from rest_framework import serializers
from news.models import Category
from news.define import APP_VALUE_STATUS_CHOICE
from django.utils.text import slugify

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(max_length=100, read_only=True)
    is_homepage = serializers.BooleanField(default=False)
    status = serializers.ChoiceField(choices=[choice[0] for choice in APP_VALUE_STATUS_CHOICE])
    ordering = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'is_homepage', 'status', 'ordering']
        read_only_fields = ['id', 'slug']

    def validate(self, data):
        """
        Custom validation for the serializer.
        """
        name = data.get('name')
        slug = slugify(name)
        status = data.get('status')
        
        instance = self.instance

        # Check if a category with this name already exists (excluding current instance)
        if instance and instance.name != name and Category.objects.filter(name=name).exists():
            raise serializers.ValidationError("A category with this name already exists.")

        # Check if a category with this slug already exists (excluding current instance)
        if instance and instance.slug != slug and Category.objects.filter(slug=slug).exists():
            raise serializers.ValidationError("A category with this slug already exists.")

        # Check if status is valid
        if status not in [choice[0] for choice in APP_VALUE_STATUS_CHOICE]:
            raise serializers.ValidationError("Invalid status value.")

        return data

    def create(self, validated_data):
        """
        Create and return a new `Category` instance, given the validated data.
        """
        validated_data['slug'] = slugify(validated_data['name'])  # Generate slug from name
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Category` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slugify(validated_data.get('name', instance.name))  # Regenerate slug if name changes
        instance.status = validated_data.get('status', instance.status)
        instance.ordering = validated_data.get('ordering', instance.ordering)
        instance.save()
        return instance
