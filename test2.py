import requests,urllib
from keys import ACCESS_TOKEN
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt


BASE_URL = 'https://api.instagram.com/v1/'

'''
Function declaration to get your own info
'''
def self_info():
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
            #print user_info['data'][0]['id']
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
    user_info = requests.get(request_url).json()

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


#function for getting the recent post of the owner of the access token:

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




#def get_comments_list()
def get_media_liked_own(): #function for retrieving the recently liked pic by the owner of the access token
    #user_id = get_user_id()
    #if user_id == None:

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
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

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
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
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



def hash_tags(list_hashtags):
    sizes=[]
    for tags in list_hashtags :
        request_url=(BASE_URL + '/tags/{tag_name}?access_token=&s' ) % (tags, ACCESS_TOKEN)
        print 'Get request url : %s' % (request_url)
        tags_info=requests.get(request_url).json()
        if  tags_info['meta']['code']==200:
         if len(tags_info['data']):

             sizes.append(int(tags_info['data']['media_count']))
             #print str(tags_info['data'][0]['media_count'])
         else:
             print 'No tag is there for this particular media!'
             exit()



     # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=list_hashtags, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()









def start_bot():
     while True:
         print '\n'
         print 'Hey! Welcome to InstaBot!'
         print 'What would you like to do :'
         print "a.Get your own details\n"
         print "b.Get details of a user by username\n"
         print "c.Get your recent post\n "
         print "d.Get the recent post of a user\n"
         print "e.Get the media recently liked by the user\n"
         print "f.Like the recent post of a user\n"
         print "g.Make a comment on the recent post of a user\n"
         print "h.fetch the comment list of the post of the user\n"
         print "i.Delete negative comments from the recent post of a user\n"
         print "j.No. of images associated with the particular hashtag\n"
         print "z.Exit"

         choice=raw_input("Enter your choice: ")
         if choice=="a":
             self_info()
         elif choice=="b":
             insta_username = raw_input("Enter the username of the user: ")
             get_user_info(insta_username)
         elif choice=="c":
             get_own_post()
         elif choice=="d":
             insta_username = raw_input("Enter the username of the user whose recent post you want to see and download: ")
             get_user_post(insta_username)
         elif choice=="e":
            get_media_liked_own()
         elif choice == "f":
             insta_username = raw_input("Enter the username of the user: ")
             like_a_post(insta_username)
         elif choice == "g":
             insta_username = raw_input("Enter the username of the user: ")
             post_a_comment(insta_username)
         elif choice =="h":
             insta_username=raw_input("enter the username whose posts comments you want to fetch : ")
             comment_list(insta_username)
         elif choice == "i":
             insta_username = raw_input("Enter the username of the user: ")
             delete_negative_comment(insta_username)
         elif choice == "j":
             list_hashtags= raw_input("enter the hashtags you want to search: ")
             hash_tags(list_hashtags)
         elif choice=="z":
             exit()
         else:
             print "invalid choice"

start_bot()