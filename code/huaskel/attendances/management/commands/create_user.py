from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import User


class Command(BaseCommand):
    help = 'Create a user with an option to add them to the teacher group'

    def add_arguments(self, parser):
        parser.add_argument('--email', help='The email for the new user', required=True)
        parser.add_argument('--username', help='The username for the new user', required=True)
        parser.add_argument('--password', help='The password for the new user', required=True)
        parser.add_argument('--first-name', help='The first name for the new user')
        parser.add_argument('--last-name', help='The last name for the new user')
        parser.add_argument('--teacher', action='store_true', help='Make this user a teacher')

    def handle(self, *args, **options):
        email = options['email']
        username = options['username']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']
        is_teacher = options['teacher']

        user = User.objects.create_user(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
        self.stdout.write(f'Successfully created user: {username}')

        if is_teacher:
            teacher_group, _ = Group.objects.get_or_create(name='Teacher')
            user.is_staff = True
            teacher_group.user_set.add(user)
            
            self.stdout.write(f'Made user {username} a teacher')
        
        user.save()
