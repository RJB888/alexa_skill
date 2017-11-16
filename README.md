# [AIM - Alexa Intelligent Messaging](https://github.com/RJB888/alexa_skill)


**Authors:**   
[John Jensen](https://github.com/thejohnjensen)    
[Marco Zangari](https://github.com/marco-zangari)   
[Robert Bronson](https://github.com/RJB888)   
[Darren Haynes](https://github.com/Darren-Haynes)



AIM is a functional way to send messages within a group.  With this skill, you can leave a message for a fellow team or family member, which they can then listen to at a later time.  As long as each person is part of the same account, they could even be in totally different places and use their Alexa-enabled device to access messages left for them.

When a group member leaves a message with the AIM service, it is persisted into a remote database and therefore does not limit the users to using the same device.

Once the messages have been heard, users can delete messages out of the database for a given person.  This is a LIFO operation - the most recent message to that person is deleted first.


This will be updated as the project progresses.

## App Navigation

To activate the Alexa skill say one of the following:

- "Alexa, use AIM"
- "Alexa, use AIM to send a message to (Name)"

This launches the skill, and intent depending on the utterance used.

To save a message say: 

- "send a message to (Name)"


To hear a message left for someone say: 

- "get messages for (Name)"

Follow Alexa's prompts and fill in the information for her to save/retrieve the message.

After hearing your message, you may say "repeat" to have Alexa repeat the message to you.

You may delete the last message saved for a given person by saying: 

- "delete message for (Name)

You can also say "help" and have Alexa give you a list of options available.




## Future goals

- Incorporate voice recognition to allow Alexa to log people in by voice and use that information to save data, limiting the amount of voice input required, and increasing security.

- Incorporate the Beta Skill builder package to use Alexa's built-in ability to prompt for messages and verify message content.

## Contributing


Contributing to this project will require you to install the necessary packages for working with Amazon Alexa Skills Development.  
 
- Clone the [repo](https://github.com/RJB888/alexa_skill)
 to your local machine

```
$ git clone https://github.com//RJB888/alexa_skill.git
```

Once downloaded, change directory into the `alexa_skill` directory

```
$ cd alexa_skill
```

Begin a new virtual environment with Python 3 and activate it.
```
alexa_skill $ python3 -m venv ENV 
```
```
alexa_skill $ source ENV/bin/activate
```


[Pip](https://pip.pypa.io/en/stable/) install this package as well as the testing set of extras into your virtual environment.

```
(ENV) alexa_skill $ mkdir lib
```
```
(ENV) alexa_skill $ pip install --target=lib rx
```
```
(ENV) alexa_skill $ pip install -e .[testing]
``` 


- Set up account with Amazon Developer Portal [here](https://developer.amazon.com)
- Set up account with AWS for Lambda access [here](https://console.aws.amazon.com)

Make sure to follow Amazon's instructions for linking your AWS skill ID with the Lambda function.

You can access our Lambda function in ```lambda_function.py``` and our intent schema and utterances in the ```intent_schema.json``` and ```utterance.txt``` files.

We built this using DynamoDB.  You may use whatever data persistence method you desire