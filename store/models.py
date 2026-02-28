from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse


# Create your models here.
class category(models.Model):
    category_name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50,unique=True)
    description=models.TextField()

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])


    def __str__(self):
        return self.category_name

class product(models.Model):
    product_name=models.CharField(max_length=150)  
    slug=models.SlugField(max_length=150,unique=True)
    description=models.TextField()
    price=models.IntegerField()
    stock=models.IntegerField()
    image=models.ImageField(upload_to='Collection')
    is_available=models.BooleanField(default=True)
    created_date=models.DateField(auto_now_add=True)
    modify_date=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(category,on_delete=models.CASCADE)

    def get_url(self):
        return reverse('single_product',args=[self.category.slug,self.slug])


    def __str__(self):
        return self.product_name

    


    
