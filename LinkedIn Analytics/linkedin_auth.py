import requests

# Set the necessary parameters
client_id = "{your_client_id}"
redirect_uri = "https://dev.example.com/auth/linkedin/callback"
scope = "r_liteprofile r_emailaddress w_member_social"
state = "fooobar"

# Build the authorization URL
authorization_url = "https://www.linkedin.com/oauth/v2/authorization"
authorization_params = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "state": state,
    "scope": scope
}
authorization_url = authorization_url + "?" + "&".join(f"{key}={value}" for key, value in authorization_params.items())

# Redirect the user to the authorization URL
print("Please visit the following URL to log in:")
print(authorization_url)

# Get the authorization code from the user after they have logged in
authorization_code = input("Authorization Code: ")

# Exchange the authorization code for an access token
access_token_url = "https://www.linkedin.com/oauth/v2/accessToken"
access_token_params = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": "{your_client_secret}"
}
response = requests.get(access_token_url, params=access_token_params)
access_token = response.json().get("access_token")

# Use the access token to make authorized requests
# Fetch user's data, such as full name, email, and profile picture

# Fetching full name
full_name_url = "https://api.linkedin.com/v2/me"
headers = {
    "Authorization": f"Bearer {access_token}"
}
response = requests.get(full_name_url, headers=headers)
full_name = response.json().get("firstName") + " " + response.json().get("lastName")

# Fetching email
email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
response = requests.get(email_url, headers=headers)
email = response.json().get("elements")[0].get("handle~").get("emailAddress")

# Fetching profile picture
profile_picture_url = "https://api.linkedin.com/v2/me?projection=(id,profilePicture(displayImage~:playableStreams))"
response = requests.get(profile_picture_url, headers=headers)
profile_picture = response.json().get("profilePicture").get("displayImage~").get("elements")[0].get("identifiers")[0].get("identifier")

# Print the fetched data
print("Full Name:", full_name)
print("Email:", email)
print("Profile Picture:", profile_picture)
