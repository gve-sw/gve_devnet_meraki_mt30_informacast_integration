# gve_devnet_meraki_mt30_informacast_integration
This demo integrates the Meraki MT30 button with Singlewire InformaCast to inform/warn pupils and teachers about an occurring shooting and when a MT30 button is pressed. Thereby, the Meraki MT30 button creates a webhook event, which is received by this script to then trigger a InformaCast notification via API. The location of the incident is dynamically added to the notification text based on the name of the associated MT30 button in the Meraki Dashboard.

## Contacts
* Ramona Renner

## Solution Components
* Singlewire InformaCast ([request trial here](https://www.singlewire.com/informacast-free-trial))
* Meraki Dashboard
* Meraki MT30 Button

## Workflow

![/IMAGES/high_level.png](/IMAGES/workflow.png)

## High Level Architecture

![/IMAGES/high_level.png](/IMAGES/high_level.png)


## Installation/Configuration
## Configure InformaCast

This script relies on a InformaCast message template, user with associated devices and distribution list. Thereby:

* **Message Template** contain the building blocks of the notifications you will send to your recipients, e.g. text, audio, confirmation responses, etc.

* **User**: Individual users are people who can view, create, send, and receive notifications, depending on their allowed permissions. Unless otherwise specified, “users” refers to individual users. 

* **Distribution List:** A collection of recipients, e.g. individual users, anonymous users, and applications, that are typically grouped together for the purposes of receiving notifications. 

1. Create a new or reuse an available user and add a SMS enabled and email device:
* [Add individual Users](https://www.singlewire.com/help/fusion/cucm/index.htm#t=InformaCast_Mobile%2FUsing%2FIndividual_Users%2FAdd_a_User.htm&rhsearch=individual%20user)
* [Add email devices to an individual user](https://www.singlewire.com/help/fusion/cucm/InformaCast_Mobile/Using/Individual_Users/Add_an_Email_Device_to_a_User.htm)
* [Add SMS-enabled devices to an individual user](https://www.singlewire.com/help/fusion/cucm/InformaCast_Mobile/Using/Individual_Users/Add_an_SMS-enabled_Device_to_a_User.htm)

2. Assign the mentioned user to a new or available distribution list:
* [Manage distribution lists](https://www.singlewire.com/help/fusion/cucm/index.htm#t=InformaCast_Mobile%2FUsing%2FDistribution_Lists%2FManage_Distribution_Lists.htm&rhsearch=distribution%20list)
* [Add individual users with the User Details Page to a distribution list](https://www.singlewire.com/help/fusion/cucm/InformaCast_Mobile/Using/Distribution_Lists/Add_Users_to_a_Distribution_List_with_the_Subscriptions_Tab.htm)

3. Create or adapt a message template:
* [Add a message template](https://www.singlewire.com/help/fusion/cucm/InformaCast_Mobile/Using/Message_Templates/Add_a_Message_Template.htm) 
* [Edit a message template](https://www.singlewire.com/help/fusion/cucm/index.htm#t=InformaCast_Mobile%2FUsing%2FMessage_Templates%2FEdit_a_Message_Template.htm)

> Hint: Both the Subject and Body fields of a message template allow dynamic text, e.g. the ability to enter a variable, such as the location a notification is sent from, and have that variable’s specific information populate the field upon sending the notification. For example, entering, “The panic button in {{affectedLocation}} was pressed.", in the Body field would result in a notification being sent with the body of, “The panic button in Room xxx - Building A - xxx School was pressed. "

## Make Local Application Reachable of the Internet

The script requires being reachable over an internet accessible URL to receive the Meraki MT30 Webhook events. Therefore, it can be deployed on different IaaS platforms like Heroku, Amazon Web Services Lambda, Google Cloud Platform (GCP) etc. . For simplicity, we use the tool ngrok here.

1. Download ngrok on the [official website](https://ngrok.com/download).
2. Extract the folder files
3. Run the ngrok.exe by double-clicking on the file
4. Type the command ngrok http 5000 and press enter
5. Note the https redirect URL for a later step

![/IMAGES/ngrok.png](/IMAGES/ngrok.png)


## Configure the Meraki Dashboard

It is required to define a Webhook HTTP server and to configure a MT30 button automation in the Meraki Dashboard for this integration.

*Configure the Webhook in the Meraki Dashboard:*

1. Go to **Network-wide** > **Alerts**

2. Add an **HTTP server** in **Webhooks: HTTP servers** section:

2.1. Fill in a **name** for your webhook, e.g. InformaCast Integration

2.2. Add [ngrok https url]/webhookreceiver in the **URL** field

2.3. Choose and fill in a **shared secret**, e.g. secret

![/IMAGES/merakiwebhook.png](/IMAGES/merakiwebhook.png)

*Configure a Meraki MT30 Button Automation*

1. Go to **Sensors** > **Configure:Automations**
2. Click the  **New Automation** button
3. Fill in a **name** for the automation (e.g. InformaCast Integration) and click **Next**
4. Choose the **Button** sensor and click **Next**
5. Choose the **Any Press** trigger and click **Next**
6. Check the **Send a Webhook command** action and add the previously defined **Webhook HTTP server** as Webhook recipient.
7. Click **Next**
8. Select the **Always** schedule and click **Next**
9. Select the all MT30 buttons to apply the automation to and click **Next**
10. Check the preview and accept the input by pressing **Finish and Save**


## Script setup

1. Make sure you have [Python 3.8.0](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed

2. Clone this Github repository into a local folder:  
  ```git clone [add github link here]```
  - For Github link: 
      In Github, click on the **Clone or download** button in the upper part of the page > click the **copy icon**  
      ![/IMAGES/giturl.png](/IMAGES/giturl.png)
  - Or simply download the repository as zip file using 'Download ZIP' button and extract it

3. Access the downloaded folder:  
  ```cd gve_devnet_meraki_mt30_informacast_integration```

4. Install all dependencies:  
  ```pip install -r requirements.txt```

5. Configure the environment variables in **.env** file:  
      
  ```python  
    APP_TOKEN="[InformaCast application API token]"
    BASE_URL="[Base URL for the InformCast API endpoints, e.g.https://api.icmobile.singlewire.com/api]"
    DISTRIBUTION_LIST_ID="[ID of distribution list to send notification to]"
    MESSAGE_TEMPLATE_ID="[ID of message template to use for notifications]"
    MERAKI_WEBHOOK_SECRET="[Webhook secret as defined for Webhook HTTP server configuration, e.g. secret]"
  ```

> Hint: Instructions on how to obtain an InformaCast API token can be found [here](https://www.singlewire.com/help/fusion/cucm/index.htm#t=InformaCast_Mobile%2FUsing%2FApplications%2FAdd_an_Application_and_Generate_a_Token.htm&rhsearch=application%20token&rhhlterm=application%20applications%20token%20tokens)]

> Hint: Get a list of all available distribution lists and their associated IDs by executing the distribution_lists.py script in the terminal via ```python3  distribution_lists.py```. Please fill in and save the APP_TOKEN and BASE_URL values before executing the script.

> Hint: Get a list of all available message templates and their associated IDs by executing the message_templates.py script in the terminal via  ```python3  message_templates.py```. Please fill in and save the APP_TOKEN and BASE_URL values before executing the script.
 
6. Run the integration application  
  ```python connector_webhook.py```

At this point, everything is set up and the application is running. 


## Usage

An email and SMS is sent to the defined InformaCast user as soon as the MT30 button is pressed. Thereby, the script output indicates when the button was pressed and the InformCast notification was sent.


# Screenshots

![/IMAGES/running.png](/IMAGES/running.png)
![/IMAGES/sms.jpg](/IMAGES/sms.jpg)
![/IMAGES/email.png](/IMAGES/email.png)


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.