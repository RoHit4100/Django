# HTTP Status Codes
HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

# Response messages
RESPONSE_SUCCESS = "Request was successful."
RESPONSE_CREATED = "Resource has been created successfully."
RESPONSE_BAD_REQUEST = "Bad request. Please check your input."
RESPONSE_NOT_FOUND = "Resource not found."
RESPONSE_INTERNAL_ERROR = "Internal server error. Please try again later."

# Pagination settings
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Restaurant Model Field Names
RESTAURANT_ID = 'id'
RESTAURANT_NAME = "name"
RESTAURANT_WEBSITE = "website"
RESTAURANT_DATE_OPENED = "date_opened"
RESTAURANT_LONGITUDE = "longitude"
RESTAURANT_LATITUDE = "latitude"
RESTAURANT_TYPE = "restaurant_type"
RESTAURANT_TYPE_CHOICES = [
        ('IN', "Indian"),
        ('IT', "Italian"),
        ('CH', "Chinese"),
        ('JP', "Japanese"),
        ('MX', "Mexican"),
        ('FR', "French"),
        ('US', "American"),
        ('MD', "Mediterranean"),
        ('TH', "Thai"),
        ('GR', "Greek"),
        ('OTH', 'Other')
    ]

# Rating Model Field Names
RATING_USER = "user"
RATING_RESTAURANT = "restaurant"
RATING_VALUE = "rating"
RATING_REVIEW = "review"

# Sale Model Field Names
SALE_RESTAURANT = "restaurant"
SALE_INCOME = "income"
SALE_DATE_TIME = "date_time"

# Email Subjects
WELCOME_EMAIL_SUBJECT = "Welcome to DEMO_APPLICATION!"

# Email Templates
WELCOME_EMAIL_MESSAGE = """
Hi {username},

Congratulations! Your account has been successfully created with DEMO_SERVICE.

We're thrilled to have you on board! Here are your next steps:

1. Login to your account: Use the link below to access your account and get started.
2. Explore our features: Discover all that we have to offer.

---

Email ID: {email_id}

If you have any questions or need assistance, feel free to reach out to our support team at support@demoapplication.com.

Best regards,  
The DEMO_APPLICATION Team
"""