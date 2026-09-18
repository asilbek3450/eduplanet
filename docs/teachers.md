# EduPlanet: o‘qituvchilar va kurslar

Superadmin `/admin/` orqali foydalanuvchi yaratadi, unga parol beradi va
**O‘qituvchi roli** belgisini tanlaydi. Instruktor profili avtomatik yaratiladi.
Ustoz haqida ma’lumotlarni **Instruktorlar** bo‘limida to‘ldirish mumkin.
O‘qituvchiga `is_staff` yoki `is_superuser` huquqi kerak emas.

O‘qituvchi oddiy kirish sahifasidan kirib, `/users/profile/` profilida o‘z
kurslarini va video darslarini yaratadi, tahrirlaydi yoki o‘chiradi.
Header barcha foydalanuvchilar uchun bir xil: **Profil**. O‘qituvchi bo‘limi
faqat admin bergan rol mavjud bo‘lganda ko‘rinadi. Eski `/teacher/` havolasi profilga yo‘naltiradi.
Profil o‘chirilsa yoki foydalanuvchi faolsizlantirilsa, kabinetga kirish yopiladi.
Profil o‘chirilganda kurslar saqlanadi; superadmin ularni boshqa ustozga biriktirishi mumkin.

`/courses/` katalogida qidiruv va yo‘nalish filtri mavjud. Yo‘nalishlarni
superadmin **Kategoriyalar** bo‘limida kengaytiradi. Kurs markazi mavjud
markazlardan tanlanadi. Kurs saqlanishi bilan ochiq katalogda ko‘rinadi.

Oldingi kurslarga ustoz va yo‘nalish avtomatik tayinlanmaydi: superadmin
**Kurslar → Tahrirlash** orqali to‘g‘ri egani va yo‘nalishni tanlaydi.
Mavjud foydalanuvchilarning parollari va superadmin huquqlari o‘zgartirilmaydi.

Deploy: `python manage.py migrate`.
Tekshirish: `python manage.py test dashboard users connections courses centers blogs`.
