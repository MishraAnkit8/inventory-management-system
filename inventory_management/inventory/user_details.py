
# from django.db import connection 


# def find_user_by_username(username: str):
#     print(f'user name in user models ====<<<<>>>>> {username}')
#     """
#     Find an active user by email using raw SQL query.
#     """
#     try:
#         with connection.cursor() as cursor:
#             print(f'username inside cursor ===<<<>>> {username}')
            
#             # Printing the query to verify it's formatted correctly
#             query = "SELECT * FROM users WHERE email = %s"
#             print(f'Executing query: {query} with username: {username}')
            
#             cursor.execute(query, [username])
            
#             # Checking if query executed successfully
#             print('Query executed successfully.')
            
#             row = cursor.fetchone()

#             if row:
#                 print(f'User found: {row}')
#                 return row
#             else:
#                 print(f'No active user with email {username}')
#                 return None
#     except Exception as e:
#         # If there's an error, it will be caught here
#         print(f'Error occurred while executing the query: {e}')
#         return None




from django.http import JsonResponse
from .models import User
from django.core.exceptions import ObjectDoesNotExist

def get_user_by_email(email):
    try:
        # Retrieve the user by email
        user = User.objects.get(email=email)
        print('user in user details models ===<<<<>>>>', user)
        return user
    except ObjectDoesNotExist:
        return None

