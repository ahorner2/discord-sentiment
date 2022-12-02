import csv
import json
import h5py
import requests
import datetime
import nltk
from vader import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()


def get_messages(channelId):
    ''' scrapes last 50 messages (rate limit) from given Disc channel ID '''

    headers = {
        # only required header is disc developer token
        'authorization': 'YOUR_TOKEN_HERE'
    }

    # Can be found throgh using Dev Tools in the web app
    response = requests.get(
        f'https://discord.com/api/v9/channels/{channelId}/messages', headers=headers)
    jsonn = json.loads(response.text)

    message_list = []

    for value in jsonn:
        messages = (value['content'])  # list form
        message_list.append(messages)  # append to string

    current_date = f'{datetime.datetime.now().strftime("%m.%d.%Y")}.csv'
    # store messages in csv (keep these human readable for reference)
    with open(current_date, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(message_list)
        file.close()

    return message_list


def vibecheck(data):
    '''Takes in parsed data and assigns a polarity score between 1 and -1'''

    score_compound = []
    # iterate through messages and assign individual polarity
    for i in range(0, len(data)):
        score = analyzer.polarity_scores(data[i])
        score_1 = score['compound']
        score_compound.append(score_1)

    avg = sum(score_compound)/len(score_compound)

    # store each combined sentiment value
    with open('avgTracker.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([avg])

    print('Individual scores: ', score_compound)
    print('-----------------------------------')
    print('Highest positive sentiment recorded: ', max(score_compound))
    print('Highest negative sentiment recorded: ', min(score_compound))
    print('The average sentiment is: ', round(avg, 4))
    print('Current sample size: ', len(score_compound))
    print('-----------------------------------')

    if avg >= 0.05:
        print('Social sentiment is positive.')

    elif (avg > -0.05) and (avg < 0.05):
        print('Social sentiment is neutral.')

    else:
        print('Social sentiment is negative.')

    # indiv score data stored as a readable csv, and a compressed h5 file
    with open('scoreMaster.csv', 'a', newline='', encoding='utf-8') as out:
        writer = csv.writer(out, delimiter=',')
        writer.writerow(score_compound)

    # assign to numpy array
    data = np.array(score_compound)

    # compress numpy array to h5 file for long-term storage
    with h5py.File('CHOOSE_FILE_NAME.h5', 'a') as h5f:
        h5f['score_compound'].resize((h5f['score_compound'].shape[0] + data.shape[0]), axis=0)
        h5f['score_compound'][-data.shape[0]:] = data


def main():

    data = get_messages('YOUR_CHANNEL_ID')

    # anaylze message polarity
    vibecheck(data)


if __name__ == "__main__":
    main()
