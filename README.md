# 🚗 RideRipple – Community Ride-Sharing Web Application

[Live Repo 🔗](https://github.com/Priyanka-Patil15/RideRipple)

**RideRipple** is a secure, community-based ride-sharing platform designed for short-distance travel. Built with Django and Leaflet.js, the system supports Riders, Drivers, and Admins with features like interactive maps, shared ride invitations, Stripe payments, and email alerts.

---

## 🛠️ Tech Stack

- **Backend**: Django (ASGI-compatible)
- **Frontend**: Django templates + Bootstrap + Leaflet.js (OpenStreetMap)
- **Database**: PostgreSQL
- **ASGI Server**: Daphne
- **Email**: SMTP (for bookings, cancellations, and reminders)
- **Payment Gateway**: Stripe
- **Testing**: pytest, pytest-django
- **Version Control**: GitHub

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Priyanka-Patil15/RideRipple.git
cd RideRipple
```

### 2. Create a virtual environment

```bash
python -m venv virtualEnv
source virtualEnv/bin/activate  # Windows: django_env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in your root directory and add:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=your_password
STRIPE_SECRET_KEY=your_stripe_secret
```

### 5. Migrate Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 🚀 Running the App

To run using **Daphne** (ASGI server):

```bash
daphne RideSafe.asgi:application
```

For development (optional):

```bash
python manage.py runserver
```

Access: [http://localhost:8000](http://localhost:8000)

---

## 🔐 Authentication Roles

- **Rider**: Book/manage rides, receive notifications  
- **Driver**: Post rides, view requests  
- **Admin**: Monitor activity, access analytics dashboard

---

## ✨ Key Features

- ✅ **Secure Login** – Role-based access for Riders, Drivers, and Admins  
- 🗺️ **Map-based Booking** – Book rides using Leaflet.js and OpenStreetMap  
- 🧑‍🤝‍🧑 **Shared Rides with Friends** –  
  Riders can invite friends to share rides. Invited users must have a profile to accept or decline invitations.  
  Shared rides include:
  - Invitation management  
  - Real-time chat between riders  
  - Visibility restricted to authorized participants  
- 💳 **Stripe Integration** – Secure online payments  
- 📊 **Admin Dashboard** – Analytics and moderation tools for platform admins  
- 🤖 **AI Help Chat** – External AI integration for user support  
- 📱 **Mobile Responsive** – Works smoothly across devices

---

## 🧪 Testing

Run all tests:

```bash
pytest
```

Test coverage includes:
- Unit Tests (Models, Views, Payment Logic)
- System Tests (Booking workflows)
- Negative Tests (Unauthorized access, invalid data)

---

## 🧾 License

This project was developed as part of the **CISC 594 – Software Testing Principles & Techniques** course at Harrisburg University.

---
