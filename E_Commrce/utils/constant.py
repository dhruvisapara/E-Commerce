# set of gender choices

MALE = "male"
FEMALE = "female"
OTHER = "other"

GENDER = ((MALE, "male"), (FEMALE, "female"), (OTHER, "other"))

# set of possible order statuses

SUBMITTED = 1
PROCESSED = 2
SHIPPED = 3
CANCELLED = 4


ORDER_STATUSES = (
    (SUBMITTED, "Submitted"),
    (PROCESSED, "Processed"),
    (SHIPPED, "Shipped"),
    (CANCELLED, "Cancelled"),
)

B2B_COMPANIES = "b2b_companies"
B2C_USERS = "b2c_user"
BUISNESS_TYPE = (
    (B2B_COMPANIES, "b2b_companies"),
    (B2C_USERS, "b2c_user"),
)

# GST registration certificate and GSTIN number of applicant’s business
# PAN card details of the business entity
# CURRENT account with bank’s name and branch
# NAME of the account holder
# ACCOUNT number and IFSC Code

#seller's form
# Seller’s name
# Email
# Phone
# Company’s name
# Nature of business
