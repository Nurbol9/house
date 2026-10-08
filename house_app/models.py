from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('seller', 'Продавец'),
        ('buyer', 'Покупатель'),
    ]
    LANG_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]

    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    preferred_language = models.CharField(max_length=2, choices=LANG_CHOICES, default='ru')

    def __str__(self):
        return self.username


class Property(models.Model):
    DEAL_CHOICES = [('sale', 'Купить'), ('rent', 'Арендовать')]
    TYPE_CHOICES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
        ('land', 'Участок'),
        ('commercial', 'Коммерческая недвижимость'),
    ]
    CURRENCY_CHOICES = [('USD', '$'), ('KGS', 'сом')]
    PRICE_TYPE_CHOICES = [('total', 'за всё'), ('per_m2', 'за м²')]
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('good', 'Хорошее'),
        ('used', 'Б/у'),
        ('repair', 'Требует ремонта'),
    ]
    HOUSE_TYPE_CHOICES = [
        ('brick', 'Кирпичный'),
        ('panel', 'Панельный'),
        ('monolith', 'Монолитный'),
        ('wood', 'Деревянный'),
    ]
    LEGAL_CHOICES = [
        ('red_book', 'Красная книга'),
        ('contract', 'Договор купли-продажи'),
        ('power_of_attorney', 'Доверенность'),
        ('other', 'Другое'),
    ]

    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='properties')

    deal_type = models.CharField(max_length=10, choices=DEAL_CHOICES, default='sale')
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)

    price = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    price_type = models.CharField(max_length=10, choices=PRICE_TYPE_CHOICES, default='total')

    area = models.DecimalField(max_digits=8, decimal_places=2, help_text='м²')
    land_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='сотки')
    rooms = models.PositiveSmallIntegerField(null=True, blank=True)
    floor = models.PositiveSmallIntegerField(null=True, blank=True)
    total_floors = models.PositiveSmallIntegerField(null=True, blank=True)
    ceiling_height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text='м')

    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True)
    house_type = models.CharField(max_length=10, choices=HOUSE_TYPE_CHOICES, blank=True)
    legal_docs = models.CharField(max_length=20, choices=LEGAL_CHOICES, blank=True)

    exchange_possible = models.BooleanField(default=False)
    installment_possible = models.BooleanField(default=False)
    mortgage_possible = models.BooleanField(default=False)
    from_owner = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    has_cadastre_report = models.BooleanField(default=False)
    video_url = models.URLField(blank=True)

    is_approved = models.BooleanField(default=False)  # модерация админом
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')

    def __str__(self):
        return f'Фото #{self.pk} — {self.property}'


class Review(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_written')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} → {self.seller}: {self.rating}'