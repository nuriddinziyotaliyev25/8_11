from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
    """
    Ovqatning turi yoki kategoriyasini ifodalovchi model.

    Maydonlar:
        title (CharField): Turi yoki kategoriyaning nomi.

    Metodlar:
        __str__: Ob'ektni satr ko'rinishida qaytaradi, bunda turi nomi sifatida qaytariladi.

    Meta:
        verbose_name: Modelning birlikdagi inson uchun tushunarli nomi - "Tur".
        verbose_name_plural: Modelning ko‘plikdagi inson uchun tushunarli nomi - "Turlar".
    """
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tur"
        verbose_name_plural = "Turlar"


class Food(models.Model):
    """
    Ovqat elementini ifodalovchi model.

    Maydonlar:
        type (ForeignKey): Ovqat elementining turi bilan bog'langan xorijiy kalit.
        title (CharField): Ovqat elementining nomi.
        ingredient (TextField): Ovqat tarkibidagi ingredientlar.
        price (DecimalField): Ovqatning narxi (6 raqamgacha, 2 kasr raqam).
        created_at (DateTimeField): Ovqat qo‘shilgan vaqtni ifodalaydi.
        updated_at (DateTimeField): Ovqat oxirgi yangilangan vaqtni ifodalaydi.

    Metodlar:
        __str__: Ob'ektni ovqat nomi sifatida qaytaradi.

    Meta:
        verbose_name: Modelning birlikdagi inson uchun tushunarli nomi - "Taom".
        verbose_name_plural: Modelning ko‘plikdagi inson uchun tushunarli nomi - "Taomlar".
        ordering: Ovqatlarni 'created_at' maydoni bo'yicha kamayuvchi tartibda tartiblaydi.
    """
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    ingredient = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Taom"
        verbose_name_plural = "Taomlar"
        ordering = ['-created_at']


class Comment(models.Model):
    """
    Ovqatga yozilgan izohni ifodalovchi model.

    Maydonlar:
        author (ForeignKey): Izoh muallifi bilan bog'liq xorijiy kalit.
        food (ForeignKey): Izoh bog'langan ovqat ob’ekti.
        text (TextField): Izohning matni.
        created_at (DateTimeField): Izoh qo'shilgan vaqt.

    Metodlar:
        __str__: Izohni muallif ismi va ovqat nomi bilan qaytaradi.

    Meta:
        verbose_name: Modelning birlikdagi inson uchun tushunarli nomi - "Izoh".
        verbose_name_plural: Modelning ko‘plikdagi inson uchun tushunarli nomi - "Izohlar".
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.get_full_name() + ' - ' + self.food.title

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"


class Favorite(models.Model):
    """
    Foydalanuvchining sevimli ovqatini ifodalovchi model.

    Maydonlar:
        user (ForeignKey): Foydalanuvchi bilan bog‘liq xorijiy kalit.
        food (ForeignKey): Foydalanuvchi tomonidan saqlangan ovqat ob’ekti.
        created_at (DateTimeField): Sevimli sifatida qo'shilgan vaqt.

    Metodlar:
        __str__: Foydalanuvchi nomi va sevimli ovqat nomi bilan qaytaradi.

    Meta:
        verbose_name: Modelning birlikdagi inson uchun tushunarli nomi - "Sevimli".
        verbose_name_plural: Modelning ko‘plikdagi inson uchun tushunarli nomi - "Sevimlilar".
        unique_together: Har bir foydalanuvchi va ovqat juftligi noyobligini ta'minlaydi.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s favorite - {self.food.title}"

    class Meta:
        verbose_name = "Sevimli"
        verbose_name_plural = "Sevimlilar"
        unique_together = ('user', 'food')
