import argparse
from github import Github, GithubException
import re

from ansicolors import *



if __name__ == '__main__':

    #Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', '-t', required=True, type=str, desc='Personal Access Token for Github')
    parser.add_argument('--verbose', type=bool, desc='Whether to print more messages to the console')

    args = parser.parse_args()

    #Configure github and current user
    g = Github(args.token)
    user = g.get_user()

    verbose = args.verbose #more readable

    follower_names = [f.login for f in user.get_followers()]
    

    #Look through each follower
    for name in follower_names:
        user = g.get_user(name)


        #Look through all the user's repos
        for repo in user.get_repos():
            #Get and print user's name and URL
            name = repo.name 
            url = repo.html_url

            if verbose:
                print(f"    Name: {name}")
                print(f"    URL: {url}")

            #Try to get a README. If the README doesn't exist, print a warning
            try:
                readme_contents = repo.get_readme().decoded_content.decode('utf-8')
                if verbose:
                    print(f"    README contents: {readme_contents}")
            except GithubException as e:
                readme_contents = None
                if verbose:
                    if e.status == 404:
                        printc(YELLOW, "    Warning: README does not exist")
                    else:
                        printc(YELLOW, "    Warning: README content fetch error")

            #Remove all non-alphanumeric characters 
            name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
            readme_contents = re.sub(r'[^a-zA-Z0-9]', '', readme_contents).lower() if readme_contents else None

            if verbose:
                print()

        