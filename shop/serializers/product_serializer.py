from rest_framework import serializers
from shop.models import Product, Category, PlantingMethod
from shop.define import APP_VALUE_STATUS_CHOICE
from django.utils.text import slugify

class ShopProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(max_length=100, read_only=True)  # Make slug read-only
    status = serializers.ChoiceField(choices=[choice[0] for choice in APP_VALUE_STATUS_CHOICE])
    ordering = serializers.IntegerField()
    special = serializers.BooleanField()
    price = serializers.DecimalField(max_digits=10, decimal_places=0)
    price_sale = serializers.DecimalField(max_digits=10, decimal_places=0, allow_null=True, required=False)
    price_real = serializers.DecimalField(max_digits=10, decimal_places=0, read_only=True)
    total_sold = serializers.IntegerField(read_only=True)
    summary = serializers.CharField()
    content = serializers.CharField()
    image = serializers.ImageField(allow_null=True, required=False)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    planting_methods_ids = serializers.PrimaryKeyRelatedField(queryset=PlantingMethod.objects.all(), many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'status', 'ordering', 'special', 'price', 'price_sale', 'price_real', 'total_sold', 'summary', 'content', 'image', 'category_id', 'planting_methods_ids']
        read_only_fields = ['id', 'slug', 'price_real', 'total_sold']

    def validate(self, data):
        """
        Custom validation for the serializer.
        """
        name = data.get('name')
        slug = slugify(name)
        status = data.get('status')
        
        instance = self.instance

        # Check if a product with this name already exists (excluding current instance)
        if instance and instance.name != name and Product.objects.filter(name=name).exists():
            raise serializers.ValidationError("A product with this name already exists.")

        # Check if a product with this slug already exists (excluding current instance)
        if instance and instance.slug != slug and Product.objects.filter(slug=slug).exists():
            raise serializers.ValidationError("A product with this slug already exists.")

        # Check if status is valid
        if status not in [choice[0] for choice in APP_VALUE_STATUS_CHOICE]:
            raise serializers.ValidationError("Invalid status value.")

        return data

    def create(self, validated_data):
        """
        Create and return a new `Product` instance, given the validated data.
        """
        validated_data['slug'] = slugify(validated_data['name'])  # Generate slug from name
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Product` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slugify(validated_data.get('name', instance.name))  # Regenerate slug if name changes
        instance.status = validated_data.get('status', instance.status)
        instance.ordering = validated_data.get('ordering', instance.ordering)
        instance.special = validated_data.get('special', instance.special)
        instance.price = validated_data.get('price', instance.price)
        instance.price_sale = validated_data.get('price_sale', instance.price_sale)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.planting_methods_ids = validated_data.get('planting_methods_ids', instance.planting_methods_ids)
        instance.save()
        return instance
