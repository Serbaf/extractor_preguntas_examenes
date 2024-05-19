# Login page
FORM_XPATH = "//div[@id='__layout']/div[1]/div[1]/div[2]/div[1]/form[1]"
LOGIN_USER_XPATH = f"{FORM_XPATH}/div[1]/div[1]/input[1]"
LOGIN_PWD_XPATH = f"{FORM_XPATH}/div[2]/div[1]/input[1]"
LOGIN_BUTTON_XPATH = f"{FORM_XPATH}/div[3]/div[1]/button[1]"

# Logged in navigation page
AGENCIES_XPATH = "//a[@href='#/agencies']"


# EdX course page
EDX_MAIN_DIV = "//main[@id='main-content']/div[1]"
EDX_TITLE = f"{EDX_MAIN_DIV}//h1"
EDX_NUM_WEEKS = f"{EDX_MAIN_DIV}//div[contains(@class, 'course-snapshot-content')]/div[1]/div[1]/div[1]/div[1]"
EDX_HOURS_PER_WEEK = f"{EDX_MAIN_DIV}//div[contains(@class, 'course-snapshot-content')]/div[1]/div[1]/div[1]/div[2]"
