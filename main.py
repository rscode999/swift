import argparse
from github import Github, GithubException
import sys
from win32com.client.dynamic import Dispatch

from utils import *




if __name__ == '__main__':

    #Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--launch', action='store_true', help='Launch instead of doing a scouting run')
    parser.add_argument('--n-msgs', '-n', type=int, help="Set the script's verbosity. Must be a positive integer")
    parser.add_argument('--verbose', '-v', action='store_true', help='Whether to print more messages to the console')

    args = parser.parse_args()

    ###################
    #Configure variables

    if args.n_msgs < 0:
        parser.error('Number of messages must be a positive integer')

    token = input("Enter Github personal access token: ")
    verbose = args.verbose #more readable


    ##################


    #Configure github and current user
    g = Github(token)
    user = g.get_user()

    #Get all followers and check for valid PAT
    try:
        follower_names = [f.login for f in user.get_followers()]
    except GithubException:
        printc(RED, "Error: Personal access token not accepted")
        sys.exit(1)
    

    #Create Outlook API reference
    outlook = Dispatch("outlook.application")


    #Look through each follower
    for name in follower_names:
        user = g.get_user(name)

        if verbose:
            print("--------------------------------------------")
            print(f'For user {name}\n')

        #Look through all the user's repos
        for repo in user.get_repos():
            #Get and print user's name and URL
            name = repo.name 
            url = repo.html_url

            if verbose:
                print(f"Checking repo {name} at {url}")

            #Try to get a README. If the README doesn't exist, print a warning
            try:
                readme_contents = repo.get_readme().decoded_content.decode('utf-8')
            except GithubException as e:
                readme_contents = None
                if verbose:
                    if e.status == 404:
                        printc(YELLOW, "README does not exist")
                    else:
                        printc(YELLOW, "README content fetch error")


            #Remove all non-alphanumeric characters and stringify
            name = remove_variants(name)
            readme_contents = remove_variants(readme_contents) if readme_contents else ''

            #check the repo
            if name.find('taylorswift')!= -1 or readme_contents.find('taylorswift') != -1:
                if verbose:
                    printc(BLUE, f'Repo {name} ({url}) has content. Launching.')
                else:
                    printc(BLUE, f'Repo {name} of {name} ({url}) has content. Launching.')
                
                #Fire!
                for i in range(args.n_msgs):
                    send_outlook_email(outlook, 'rscode999@outlook.com', 'rscode999@outlook.com',
                                    f'Content found in repo {name} ({i+1})', 'This is an automated message. Contents were found.')
                    if verbose:
                        printc(BLUE, f"Launched {i+1} of {args.n_msgs}")

            if verbose:
                print()
        
        if verbose:
            print()


    #IMPORTANT: Close the Outlook API instance
    outlook.Quit()

        