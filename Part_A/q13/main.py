import logging

# Configuring logging settings
logging.basicConfig(
    filename='tesreco.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True
)

# List to store logged-in users
login_users = []

# Function to handle login
def login(name, email):
    login_users.append(name)
    logging.info(f"{name} login with {email} email")

# Function to generate report
def report_generate(name):
    if name in login_users:
        logging.info(f"generating report for {name}")
    else:
        logging.error("error in report generating")

login("ABC", "abc@gmail.com")
report_generate("ABC")
report_generate("XYZ")