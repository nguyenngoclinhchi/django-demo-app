from rest_framework import serializers
from shop.models import Blog
from shop.define import APP_VALUE_STATUS_CHOICE
from django.utils.text import slugify

class ShopBlogSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(max_length=100, read_only=True)
    status = serializers.ChoiceField(choices=[choice[0] for choice in APP_VALUE_STATUS_CHOICE])
    ordering = serializers.IntegerField()
    special = serializers.BooleanField()
    publish_date = serializers.DateTimeField()
    content = serializers.CharField()
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Blog
        fields = ['id', 'name', 'slug', 'status', 'ordering', 'special', 'publish_date', 'content', 'image']
        read_only_fields = ['id', 'slug']

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
        Create and return a new `Blog` instance, given the validated data.
        """
        validated_data['slug'] = slugify(validated_data['name'])  # Generate slug from name
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Blog` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slugify(validated_data.get('name', instance.name))  # Regenerate slug if name changes
        instance.status = validated_data.get('status', instance.status)
        instance.ordering = validated_data.get('ordering', instance.ordering)
        instance.special = validated_data.get('special', instance.special)
        instance.publish_date = validated_data.get('publish_date', instance.publish_date)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
