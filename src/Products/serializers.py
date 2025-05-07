from rest_framework import serializers
from .models import Product , Comments , Discount , Rating
from django.db.models import Avg



class CommentsSerializer(serializers.ModelSerializer):
    """
    serializer for user comments
    """
    product_name = serializers.CharField(source='product.name' , read_only=True)
    product_image = serializers.ImageField(source='product.image' , read_only=True)

    class Meta :
        model = Comments
        fields = '__all__'


class AddProductSerializer (serializers.ModelSerializer):
    """
        serializer for vandors that add product 
    """
    class Meta :
        model = Product
        fields = [
            'category','name','description','price','stock','image'
        ]


class EditProductSerializer (serializers.ModelSerializer):
    """
        serializer for editing vendor`s product with validator for discount
    """
    discount_amount = serializers.DecimalField(max_digits=6 , decimal_places=2 , required=False , allow_null=True)

    discount_percentage = serializers.DecimalField(max_digits=4 , decimal_places=2 , required=False , allow_null=True)
    class Meta :
        model = Product
        fields = [
            'category','name','description','price','stock','image' , 'discount_amount' , 'discount_percentage'
        ]

    def validate(self, data):
        discount_amount = data.get('discount_amount')
        discount_percentege = data.get('discount_percentage')

        if discount_amount and discount_percentege :
            raise serializers.ValidationError("just input one of the discount type !")
        
        return data
    
    def update(self, instance, validated_data):
        discount_amount = validated_data.pop('discount_amount' , None)
        discount_percentege = validated_data.pop('discount_percentage' , None)

        instance = super().update(instance , validated_data)

        if discount_amount is not None :
            Discount.objects.update_or_create(
                product=instance,
                defaults={'amount':discount_amount , 'is_percentage':False}
            )

        elif discount_percentege is not None :
            Discount.objects.update_or_create(
                product=instance,
                defaults={'amount':discount_percentege , 'is_percentage':True}
            )

        else :
            Discount.objects.filter(product=instance).delete()

        return instance


class VendorProductSerializer (serializers.ModelSerializer):
    """
        serializer for show shop products
    """
    class Meta :
        model = Product
        fields = [
            'category','name','description','price','stock','image','id'
        ]


class SearchProductSerializer (serializers.ModelSerializer):
    """
        serializer for show all product info
    """
    final_price = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()


    class Meta :
        model = Product
        fields = ['category','name','description','price','stock','image','id','final_price','average_rating','shop_name']
        
    def get_final_price (self , obj):
        return obj.final_price()
    
    def get_shop_name (self , obj):
        return obj.store_name.name
    
    def get_category (self , obj):
        return obj.category.name



class GetSingleProductCommentsSerializer(serializers.ModelSerializer):
    """
        serializer for show all comment for one product
    """
    customer_name = serializers.SerializerMethodField()

    class Meta :
        model = Comments
        fields = ['customer_name','comment','status' ,'created_at']
    
    def get_customer_name (self , obj):
        return obj.customer.username


class SingleProductSerializer (serializers.ModelSerializer):
    """
        serializer for show one product detail
    """
    class Meta :
        model = Product
        fields =['id','category','name','description','price','store_name','image','stock','average_rating']


class SendCommentsForProductSerializer(serializers.ModelSerializer):
    """
        serializer for send comment for one product
    """
    class Meta :
        model = Comments
        fields = ['comment','status']


class ShowProductForRatingSerializer(serializers.ModelSerializer):
    """
        show single product for rating
    """
    product_name = serializers.CharField(source='name', read_only=True)
    product_image = serializers.ImageField(source='image', read_only=True)
    
    class Meta :
        model = Product
        fields = ['id','product_name','product_image']


class SendRatingForProductSerializer(serializers.ModelSerializer):
    """
        serializer for send rating for product with get avg for ratings and validate rate
    """
    class Meta :
        model = Rating
        fields = ['product','rating']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("امتیاز باید بین 1 و 5 باشد.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        rating = Rating.objects.create(customer=user, **validated_data)

        product = validated_data['product']
        rate = product.product_rating.all()
        avg_rating = rate.aggregate(Avg('rating'))['rating__avg']
        product.average_rating = avg_rating
        product.save()

        return rating