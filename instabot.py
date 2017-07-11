import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt  # used for plotting graphs or pie charts, pictorial representations
from keys import ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'


def self_info():      #this is for getting info of the owner of the access token
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:  # or user_info['meta']['code']== 304:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 or 304 received!'

'''
Function declaration to get the ID of a user by username
'''

def get_user_id(insta_username):

    request_url =(BASE_URL +'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']

        else:
            return None
    else:
        print 'Status code other than 200 or 304 received!'
        exit()

'''
Function declaration to get the info of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()  #json objects are for getting data

    if user_info['meta']['code'] == 200 : #or user_info['meta']['code']== 304:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 or 304 received!'

'''
function for getting the recent post of the owner of the access token
'''

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'yay! Your image has been downloaded!'
        else:
            print 'oops! Post does not exist!'
    else:
        print 'Status code other than 200 received!'

'''
this functions is for getting the recently uploaded post if the user 
'''

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s'%(request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            #media_id = user_media['data'][0]['id']
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


def get_media_liked_own(): #function for retrieving the recently liked pic by the owner of the access token

    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % ( ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    payload = {"access_token": ACCESS_TOKEN}
    user_media_liked = requests.get(request_url ,payload).json()

    if user_media_liked['meta']['code'] == 200:
        if len(user_media_liked['data']):
            image_name = user_media_liked['data'][0]['id'] + '.jpeg'
            image_url = user_media_liked['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return user_media_liked['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

'''
this function gets the post_id of the post of the given username 
'''

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

'''
this function is for liking a post
'''

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

'''
this function is to ppost a comment on a particular post of the user
'''

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print "POST's request url : %s" % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

'''
this function is to delete the negative comments of the particular user's particular post 
'''

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']

                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos or comment_text=='not good' or comment_text=='hate' or comment_text=='bad' ):

                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'

                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

'''
this function gets the comment list on a particular post
'''

def comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_comments = requests.get(request_url).json()
    if user_comments['meta']['code'] == 200:
        if len(user_comments['data']):
            for x in range(0, len(user_comments['data'])):
                print user_comments['data'][x]['text']
        else:
            print "there are no comments on the post"
    else:
        print 'Status code other than 200 received!'

'''
this function is to get the id of the user which is searched
'''

def user_search(insta_username):

    request_url=(BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    Q=requests.get(request_url).json()

    if Q['meta']['code']==200:
        if len(Q['data']):
            for x in range (0,len(Q['data'])):
                search = Q['data'][x]['id']
                print "The users with this username is: %s\n" % search

        else:
            print 'No results found for this user!'
    else:
        print 'Status code other than 200 received!'


def hash_tag():
    i = 0
    tags = []
    tag_name = []
    while i < 3:

        tag = raw_input("enter the hashtag : ")

        request_url = ('https://api.instagram.com/v1/tags/%s?access_token=%s') % (tag, ACCESS_TOKEN)
        tag_name.append(tag)
        print tag_name
        print 'GET request url : %s' % (request_url)
        hash_items = requests.get(request_url).json()

        if hash_items['meta']['code'] == 200:
            if len(hash_items['data']):  # implementation of how to fetch the hashtag data!

                print hash_items['data']['media_count']
                tags.append(hash_items['data']['media_count'])
                print tags
                i = i + 1


            else:
                print 'Status code other than 200 received!'

        else:
            exit()
    return tags

# def pie_chart():
#     # Pie chart, where the slices will be ordered and plotted counter-clockwise:
#     labels =
#     sizes = hash_tag()
#     fig1, ax1 = plt.subplots()
#     ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
#             shadow=True, startangle=90)
#     ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#
#     plt.show()





'''
this is the function in which menu is displayed and other functions are called
'''

def start_bot():
     while True:
         print '\n'
         print 'Hey! Welcome to InstaBot!'
         print 'What would you like to do :'
         print "a.Get your own details\n"
         print "b.Get details of a user by username\n"
         print "c.Get your recent post\n "
         print "d.Get the recent post of a user\n"
         print "e.Get the media recently liked by you\n"
         print "f.Like the recent post of a user\n"
         print "g.Make a comment on the recent post of a user\n"
         print "h.fetch the comment list of the post of the user\n"
         print "i.Delete negative comments from the recent post of a user\n"
         print "j. Search the user by username\n"
         print "k. Wana see which is the most popular foodchain? enter any 5 among which you want to compare!\n"


         print "z.Exit\n"

         choice=raw_input("Enter your choice: ")
         if choice=="a":
             self_info()
         elif choice=="b":
             insta_username = raw_input("Enter the username of the user whose details you want to fetch: ")
             if len(insta_username) > 0:

                 if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                     print "Invalid name."
                 else:
                     print "Valid name!"
                     get_user_info(insta_username)

         elif choice=="c":
             get_own_post()
         elif choice=="d":
             insta_username = raw_input("Enter the username of the user whose recent post you want to see and download: ")
             if len(insta_username) > 0:

                 if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                     print "Invalid name."
                 else:
                     print "Valid name!"
                     get_user_post(insta_username)
         elif choice=="e":
            get_media_liked_own()
         elif choice == "f":
             insta_username = raw_input("Enter the username of the user whose recent post you to like: ")
             if len(insta_username) > 0:

                 if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                     print "Invalid name."
                 else:
                     print "Valid name!"
                     like_a_post(insta_username)
         elif choice == "g":
             insta_username = raw_input("Enter the username of the user on whose recent post you want to post a comment: ")
             if len(insta_username) > 0:

                 if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                     print "Invalid name."
                 else:
                     print "Valid name!"
                     post_a_comment(insta_username)
         elif choice =="h":
             insta_username=raw_input("Enter the username whose recent post's comment_list you want to fetch : ")
             if len(insta_username) > 0:

                 if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                     print "Invalid name."
                 else:
                     print "Valid name!"
                     comment_list(insta_username)
         elif choice == "i":
             insta_username = raw_input("Enter the username of the user whose recent post's negative comments you want to delete: ")
             if len(insta_username) > 0:

                 if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                     print "Invalid name."
                 else:
                     print "Valid name!"
                     delete_negative_comment(insta_username)
         elif choice == "j":
             insta_username = raw_input("Enter the username of the user you want to search: ")
             if len(insta_username) > 0:

                 if set('[~!@#$%^&*()+{}":;\']+$ " "').intersection(insta_username):
                     print "Invalid name."
                 else:
                     print "Valid name!"
                     user_search(insta_username)



         elif choice == "k":

             hash_tag()





         elif choice=="z":
             exit()
         else:
             print "invalid choice"

start_bot()