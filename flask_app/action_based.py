from threading import Thread
import sliding_window
import json
import time
from multiprocessing import Process, Pipe


class Observer:
    Infleunce_Set = {}
    model = {}
    score = {}

    def update(self, obj, *args, **kwargs):
        raise NotImplementedError


class Model(Observer):

    model = {}
    Infleunce_Set = {}
    score = {}
    information = {}
    results = {}

    node, edge = [], []

    def __init__(self, followersFrom, followersTo, verified, isFollowersFilter, top, tweetScore, tableName, pqueue, window_size, update_interval):
        super().__init__()
        self.model = {}
        self.Infleunce_Set = {}
        self.score = {}
        self.information = {}
        self.followersFrom = followersFrom
        self.followersTo = followersTo
        self.verified = verified
        self.isFollowersFilter = isFollowersFilter
        self.top = top
        self.tweetScore = tweetScore
        self.node = []
        self.edge = []
        self.tableName = tableName
        self.pqueue = pqueue
        self.window_size = window_size
        self.update_interval = update_interval

    def update(self, obj, *args, **kwargs):
        print('notified!')
        Thread(target=self.process(obj, *args, **kwargs)).start()

    def process(self, obj, *args, **kwargs):
        print(f'Handling.....')
        if len(args) > 1:
            """print('\nremoved data that remove the old actions ', args[0])
            print('\nwrote removed_data')
            print('\nprev window ', args[1])
            print('\nwrote prev_window')
            print('\nadded data the new data added to the window ', args[2])
            print('\nwrote added_data')"""

            self.remove(args[0])
            self.influence_set_remove(args[0], args[1])
            self.insert(args[2])
            self.influence_set_insert(args[2])
            # input top k as parameter
            self.influence_score_new(self.Infleunce_Set, self.top)
        else:
            self.insert(args[0])
            self.influence_set_insert(args[0])
            # input top k as parameter
            self.influence_score_new(self.Infleunce_Set, self.top)

    def remove(self, old_action):
        # Remove the old actions from the self.model
        for i in old_action:
            if i in self.model:
                if not self.model[i]:
                    del self.model[i]  # empty
                else:
                    if len(self.model[i]) == 1:
                        if self.model[i][0] == '**root**':
                            del self.model[i]
                        else:
                            if self.model[i][0] in old_action:
                                del self.model[i]
                    else:
                        for j in self.model[i]:
                            if j in old_action:
                                self.model[i].remove(j)

    def insert(self, temp_process):
        # Insert the action in the self.model
        for index in range(len(temp_process)):
            action = str(temp_process[index]['Action_id'])
            causality_action = str(temp_process[index]['Causality_id'])

            if action not in self.model:
                # add action in self.model (adjency list)
                self.model[action] = []

            # if action is none then this is an original tweet
            if causality_action == 'None':
                self.model[action].append('**root**')  # This is the root
            else:
                # Important hint: this may be delete it when we have a real dataset
                if causality_action not in self.model:
                    self.model[causality_action] = ['**root**']
                    self.model[causality_action].append(action)
                else:
                    self.model[causality_action].append(action)

    def influence_set_insert(self, temp_process):
        # Insert
        B = 1000  # the precentage of the importance of the favorite counts with the socres
        for i in range(len(temp_process)):
            # Vairbles are from the window
            action_user = str(temp_process[i]['Action_Username'])
            causality_action = str(temp_process[i]['Causality_id'])
            causality_user = str(temp_process[i]['Causality_Username'])
            action_type = temp_process[i]['Action_Type']
            # favorite count
            favorite = (temp_process[i]['favourites_count'])
            follower = (temp_process[i]['followers_count'])
            verified = (temp_process[i]['verified'])
            text = (temp_process[i]['text'])
            coordinates = (temp_process[i]['coordinates'])
            self.information[action_user] = [
                follower, verified, text, coordinates]

            if action_user in self.Infleunce_Set and causality_action == 'None':
                for j in range(len(self.Infleunce_Set[action_user])):
                    # Update: maybe a loop to search
                    if action_user not in self.Infleunce_Set[action_user][j][0]:
                        action_type = action_type + (favorite / B)
                        self.Infleunce_Set[action_user].append(
                            (action_user, action_type))  # Append tuple
                        break
                    else:
                        if self.Infleunce_Set[action_user][j][
                                1] <= action_type:  # If the action type have the high prority will change
                            self.Infleunce_Set[action_user].remove(
                                self.Infleunce_Set[action_user][j])  # remove low prority
                            # action type +(favorite count/1000)
                            action_type = action_type + (favorite / B)
                            self.Infleunce_Set[action_user].append(
                                (action_user, action_type))  # Append tuple
                            break

            if action_user not in self.Infleunce_Set:
                action_type = action_type + (favorite / B)
                self.Infleunce_Set[action_user] = [
                    (action_user, action_type)]  # new as a tuple

            if causality_action != 'None':
                flag = False
                for j in range(i):
                    action = str(temp_process[j]['Action_id'])
                    if causality_action == action:
                        flag = True
                        for k in range(len(self.Infleunce_Set[temp_process[j]['Action_Username']])):
                            # if 'u2' in influenceSet['u1'][i][0]:
                            # Update: maybe a loop to search
                            # list out of range
                            if action_user not in self.Infleunce_Set[action_user][k][0]:
                                action_type = action_type + (favorite / B)
                                self.Infleunce_Set[temp_process[j]['Action_Username']].append(
                                    (action_user, action_type))  # Append tuple
                                break
                            else:
                                if self.Infleunce_Set[temp_process[j]['Action_Username']][k][
                                        1] <= action_type:  # If the action type have the high prority will change
                                    self.Infleunce_Set[temp_process[j]['Action_Username']].remove(
                                        self.Infleunce_Set[temp_process[j]['Action_Username']][k])  # remove low prority
                                    action_type = action_type + (favorite / B)
                                    self.Infleunce_Set[temp_process[j]['Action_Username']].append(
                                        (action_user, action_type))  # Append tuple
                                    break

                if flag == False:  # causality_action not in the window
                    # causality_action in the model
                    if causality_action in self.model and '**root**' in self.model[causality_action]:
                        if causality_user in self.Infleunce_Set:  # causality_action all ready in the influnce set
                            for j in range(len(self.Infleunce_Set[causality_user])):
                                # Update: maybe a loop to search
                                if action_user not in self.Infleunce_Set[causality_user][j][0]:
                                    action_type = action_type + (favorite / B)
                                    self.Infleunce_Set[causality_user].append(
                                        (action_user, action_type))  # Append tuple
                                    break
                                else:
                                    if self.Infleunce_Set[causality_user][j][
                                            1] <= action_type:  # If the action type have the high prority will change
                                        self.Infleunce_Set[causality_user].remove(
                                            self.Infleunce_Set[causality_user][j])  # remove low prority
                                        action_type = action_type + \
                                            (favorite / B)
                                        self.Infleunce_Set[causality_user].append(
                                            (action_user, action_type))  # Append tuple
                                        break

                        else:  # causality_action not in influence set and need to add
                            action_type = action_type + (favorite / B)
                            # Update: the causality user action type will got it from rawan stream data
                            self.Infleunce_Set[causality_user] = [
                                (causality_user, self.tweetScore), (action_user, action_type)]

    def influence_set_remove(self, old_action, old_window):
        # remove
        for i in old_action:
            flag = False
            # Check if the old action is not an influencer because if not we will remove it
            for j in range(len(old_window)):
                causality_action = str(old_window[j]['Causality_id'])
                action_id = str(old_window[j]['Action_id'])
                i = str(i)
                if i == causality_action:
                    if action_id not in old_action:
                        flag = True  # Mean will not remove it
                        break
            if flag == False:
                for k in range(len(old_window)):
                    if old_window[k]['Action_id'] == i:
                        causality_id = str(old_window[k]['Causality_id'])
                        action_user = str(old_window[k]['Action_Username'])
                        if causality_id == 'None':
                            if old_window[k]['Action_Username'] in self.Infleunce_Set and self.Infleunce_Set[old_window[k]['Action_Username']]:
                                for j in range(len(self.Infleunce_Set[action_user])):
                                    if action_user in self.Infleunce_Set[action_user][j][0]:
                                        self.Infleunce_Set[action_user].remove(
                                            self.Infleunce_Set[action_user][j])
                                        break
                        else:
                            causality_username = str(
                                old_window[k]['Causality_Username'])
                            for j in range(len(self.Infleunce_Set[causality_username])):
                                # if not then it was removed #Update: maybe a loop to search
                                if action_user in self.Infleunce_Set[causality_username][j][0]:
                                    # Update: must compare it as a tuple to remove from influence set
                                    self.Infleunce_Set[causality_username].remove(
                                        self.Infleunce_Set[causality_username][j])
                                    break

    def influence_score(self, top_k):

        for i in self.Infleunce_Set:
            i = str(i)
            self.score[i] = len(self.Infleunce_Set[i])

        self.score = sorted(self.score.items(),
                            key=lambda x: x[1], reverse=True)
        top = {}
        for i in range(top_k):
            top[self.score[i][0]] = self.score[i][1]
        self.score = top
        # print('score: ', self.score)

    def influence_score_new(self, influence, top_k):

        for i in influence:
            i = str(i)
            temp = 0
            for j in influence[i]:
                temp += j[1]
            self.score[i] = temp

        self.score = sorted(self.score.items(),
                            key=lambda x: x[1], reverse=True)
        top = {}
        counter = 0
        for i in range(len(self.score)):
            user = self.score[i][0]
            if user in self.information:
                if self.verified and self.information[user][1]:  # true
                    if (self.isFollowersFilter):  # true follower
                        if (self.followersTo != 0):
                            if self.information[user][0] >= self.followersFrom and self.information[user][0] <= self.followersTo:
                                top[self.score[i][0]] = self.score[i][1]
                                counter += 1
                        else:
                            if self.information[user][0] >= self.followersFrom:
                                top[self.score[i][0]] = self.score[i][1]
                                counter += 1
                    else:  # false follower
                        top[self.score[i][0]] = self.score[i][1]
                        counter += 1
                else:  # false
                    if (self.isFollowersFilter):  # true follower
                        if (self.followersTo != 0):
                            if self.information[user][0] >= self.followersFrom and self.information[user][0] <= self.followersTo:
                                top[self.score[i][0]] = self.score[i][1]
                                counter += 1
                        else:
                            if self.information[user][0] >= self.followersFrom:
                                top[self.score[i][0]] = self.score[i][1]
                                counter += 1
                    else:  # false follower
                        top[self.score[i][0]] = self.score[i][1]
                        counter += 1

            if counter == top_k:
                break
        self.score = top
        self.results = json.dumps(self.score)

        self.front_end(influence, self.score)

    def front_end(self, influence, result):
        global node, edge
        self.node = []
        self.edge = []
        for i in result:
            for j in influence:
                if i == j:
                    temp = {}
                    temp['name'] = i
                    temp['id'] = i
                    temp['score'] = result[i]
                    if i in self.information:
                        temp['coordinates'] = self.information[i][3]
                    self.node.append(temp)

                    for k in influence[j]:
                        temp = {}
                        temp['sourceID'] = i
                        temp['targetID'] = k[0]
                        self.edge.append(temp)
        data_dict = {
            'nodes': self.node,
            'edges': self.edge,
            'minFollowers': self.followersFrom,
            'maxFollowers': self.followersTo,
            'isVerified': self.verified,
            'top_k': self.top,
            'window_size': self.window_size,
            'update_interval': self.update_interval
        }
        self.pqueue.put(data_dict)
        print('sent data to server')
