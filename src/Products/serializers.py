from rest_framework import serializers
from .models import Product , Reviews , Discount


class ReviewsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name' , read_only=True)
    product_image = serializers.ImageField(source='product.image' , read_only=True)

    class Meta :
        model = Reviews
        fields = '__all__'


class AddProductSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = [
            'category','name','description','price','stock','image'
        ]


class EditProductSerializer (serializers.ModelSerializer):
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


class ShowSingleSerializer(serializers.ModelSerializer):
    discount_amount = serializers.DecimalField(max_digits=6 , decimal_places=2 , required=False , allow_null=True)

    discount_percentage = serializers.DecimalField(max_digits=4 , decimal_places=2 , required=False , allow_null=True)
    class Meta :
        model = Product
        fields = ['category','name','description','price','stock','image','discount_amount','discount_percentage']


class VendorProductSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = [
            'category','name','description','price','stock','image','id'
        ]


class VendorSetProductSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = [
            'name','description' , 'price','stock','rating','store_name' , 'image'
        ]
        read_only_fields =[
            'name','description' , 'price','stock','rating','store_name' , 'image'
        ]



class AllProductSerializer (serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()

    class Meta :
        model = Product
        fields = ['category','name','description','price','stock','image','id','final_price','rating','shop_name']
        
    def get_final_price (self , obj):
        return obj.final_price()
    
    def get_shop_name (self , obj):
        return obj.store_name.name
    



class SingleProductReviewsSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    class Meta :
        model = Reviews
        fields = ['customer_name','rating','comment','status']
    
    def get_customer_name (self , obj):
        return obj.customer.username

    

class SingleProductSerializer (serializers.ModelSerializer):
    class Meta :
        model = Product
        fields =['category','name','description','price','image','stock','rating','store_name']
