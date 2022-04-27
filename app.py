import requests
import json

#insert your github auth token
GITHUB_AUTH_TOKEN = ''

def getAllRepos():
    res = requests.get('https://hackodex.herokuapp.com/api/v1/getAllRepo')
    data = res.json()
    return data

def getContributors(name):
    #assuming a repo has no more than 100 contributors
    headers = {
        'Authorization': GITHUB_AUTH_TOKEN
    }
    res = requests.get('https://api.github.com/repos/{repo_name}/contributors?page=1&per_page=100'.format(repo_name=name), headers=headers)
    data = res.json()
    return data

def getUserInfo(uid):
    headers = {
        'Authorization': GITHUB_AUTH_TOKEN
    }
    res = requests.get('https://api.github.com/user/{user_id}'.format(user_id=uid), headers=headers)
    data = res.json()
    return data

def collectionLogic():
    repos = getAllRepos()
    participants = []
    partids = []
    # print(repos)
    for i in repos:
        print(i['full_name'])
        i['contributors']=createListOfParticipants(participants, partids, i['full_name'])

    print('project list:')
    print(json.dumps(repos, indent=4))

    f=open('projects.json', 'w')
    f.write(json.dumps(repos, indent=4))
    f.close()
    
    print('participants list:')    
    print(participants)
    
    f=open('participants.json', 'w')
    f.write(json.dumps(participants, indent=4))
    f.close()

def createListOfParticipants(participants, partids, reponame):
    participants_local = []
    contri = getContributors(reponame)
    for i in contri:
        if i['id'] not in partids:
            uinfo = getUserInfo(str(i['id']))
            partids.append(i['id'])
            participants.append(uinfo)
            participants_local.append(uinfo)
        else:
            for j in participants:
                if j['id']==i['id']:
                    participants_local.append(j)
                    break

    return participants_local


def main():
    # print(json.dumps(getAllRepos(), indent=4))
    # print(json.dumps(getContributors('Tilakraj0308/Calculator'), indent=4))
    # print(json.dumps(getUserInfo('45957713'), indent=4))
    collectionLogic()

if __name__ == '__main__':
    main()