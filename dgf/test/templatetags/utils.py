from ...models import Course, Friend, FavoriteCourse


def create_courses(course_names):
    new_courses = []

    for name in course_names:
        new_course = Course.objects.create(name=name)
        new_courses.append(new_course)

    return new_courses


def create_friends(usernames, favorite_courses=(), ratings=None):
    new_friends = []

    if type(favorite_courses) != list:
        favorite_courses = [favorite_courses for _ in range(len(usernames))]

    if type(ratings) != list:
        ratings = [ratings for _ in range(len(usernames))]

    for i, username in enumerate(usernames):

        new_friend = Friend.objects.create(username=username, rating=ratings[i])

        for course in favorite_courses[i]:
            if isinstance(course, Course):
                favorite = FavoriteCourse.objects.create(course=course, friend=new_friend)
                new_friend.favorite_courses.add(favorite)

        new_friends.append(new_friend)

    return new_friends
