import sys

from ytcr.__main__ import run

if __name__ == "__main__":
    email = input("Enter the Email: ")
    password = input("Enter the Password: ")
    if not email or not password:
        print(f'Email or Password is Required, Existing...!')
        sys.exit(1)

    inc_video_id = str(input("Include Video ID (Optional): "))
    if not inc_video_id:
        inc_video_id = []
    else:
        inc_video_id = inc_video_id.split(',')

    exc_video_id = str(input("Exclude Video ID (Optional): "))
    if not exc_video_id:
        exc_video_id = []
    else:
        exc_video_id = exc_video_id.split(',')

    run(email, password, inc_video_id, exc_video_id)
