import requests
from bs4 import BeautifulSoup
import requests
import json

# Set your Notion API key
api_key = "secret_XOUiYJAJE1o6YOjXUbrzOBae1kZfRTC1xYBd4ie2Ewo"
# Set the database ID
database_id = '7ef99d75e6084fc89d194cb0b04ef8e7'

#leetcode_url = input()

def outer(leetcode_url):

    def extract_leetcode_info(url):
        # Send a GET request to the provided URL
        response = requests.get(url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the problem name
        # problem = soup.find('span', class_='mr-2 text-xl font-medium leading-8 text-label-1 dark:text-dark-label-1').text.strip()
        problem = soup.find('span', class_='mr-2').text.strip()

        problem_name = problem.split('.')[1]
        # Extract the problem number
        problem_number = problem.split('.')[0]
        # Extract the problem description
        # Find the div containing the problem description
        description_div = soup.find('div', class_='_1l1MA')

        # Find all the paragraphs within the description div
        paragraphs = description_div.find_all('p')

        # Filter out paragraphs after the paragraph containing "<p>&nbsp;</p>"
        filtered_paragraphs = []
        for paragraph in paragraphs:
            if paragraph.string and paragraph.string.split(' ')[0] == 'Example':
                break
            filtered_paragraphs.append(paragraph.text.strip())

        # Join the filtered paragraphs into a single string
        problem_description = "\n".join(filtered_paragraphs)

        # problem_description = soup.find('div', class_='_1l1MA').find('p').text.strip()
        problem_difficulty = soup.find('div', class_='mt-3').find('div').text.strip()

        # problem_description = soup.find('div', class_='css-13iwqin').text.strip()

        # Return the extracted information as a dictionary
        return {
            'name': problem_name,
            'number': problem_number,
            'description': problem_description,
            'difficulty': problem_difficulty.lower(),
        }

    info = extract_leetcode_info(leetcode_url)
    problem_name = info['name']
    problem_number = info['number']
    problem_description = info['description']
    problem_difficulty = info['difficulty']

    print('Problem Name:', problem_name)
    print('Problem Number:', problem_number)
    print('Problem Description:', problem_description)
    print('Problem Difficulty:', problem_difficulty)

    # Set the Notion API endpoint for retrieving a database
    endpoint_database = f'https://api.notion.com/v1/databases/{database_id}'
    endpoint_pages = f'https://api.notion.com/v1/pages'
    endpoint_query = f'https://api.notion.com/v1/databases/{database_id}/query'
    # Set the headers with the API key and content type
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    exist = False
    payload = {
        'filter': {
            'property': 'Problem',
            'Problem': {
                'equals': problem_number
            }
        }
    }
    response = requests.post(endpoint_query.format(database_id=database_id), headers=headers, data=json.dumps(payload))
    # Check the response status
    if response.status_code == 200:
        # Get the response JSON data
        data = response.json()

        # Check if any results were found
        if data.get('results'):
            # A page with the specified problem number exists
            print('A page with the problem number exists.')
            exist = True
        else:
            # No page with the specified problem number exists
            print('No page with the problem number exists.')
    else:
        # Query request failed
        print('Failed to query pages:', response.json())


    option_id = ''
    color = ''
    if problem_difficulty == 'Easy':
        option_id = 'iui['
        color = 'green'
    elif problem_difficulty == 'Medium':
        option_id = 'Wk\t'
        color = 'purple'
    elif problem_difficulty == 'Hard':
        option_id = 'D=mB'
        color = 'red'
    # Set the properties of the new record
    new_record = {
        'parent': {'database_id': database_id},
        'properties': {
            'Problem': {'number': int(problem_number)},
            'Name': {'title': [{'text': {'content': problem_name}}]},
            'Link': {'url': leetcode_url},
            'Difficulty': {
                'select' : {
                    'name': problem_difficulty
                }
            }
        }
    }


    if not exist:
    # Send a POST request to create the new record
        response = requests.post(endpoint_pages, json=new_record, headers=headers)

        # Get the JSON response
        json_response = response.json()

        # Print the response
        # print(json_response)
        block_id = json_response['id']
    else:
        print('A page with the problem number exists.')   


    def heading_2(title):
        return  {
            'object': 'block',
            'type': 'heading_2',
            'heading_2': {
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': title,
                        }
                    }
                ]
            }
        }
    def paragraph(content):
        return  {
            'object': 'block',
            'type': 'paragraph',
            # 'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': 'Implement a Queue by linked list. Support the following basic methods:', 'link': None},
            'paragraph': {
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': content,
                        }
                    }
                ]
            }
        }


    def code():
        return  {
            'object': 'block',
            'type': 'code',
            # 'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': 'Implement a Queue by linked list. Support the following basic methods:', 'link': None},
            'code': {
                'caption': [
                    {
                        'type': 'text',
                        'text': {
                            'content': 'O(N) time complexity',
                        }
                    }
                ],
                'rich_text': [
                    {
                        'type': 'text',
                        'text': {
                            'content': ''
                        }
                    }
                ],
                'language': 'python'
            }
        }

    block_content = [

        heading_2("Problem"),
        paragraph(problem_description),
        heading_2("Discussion"),
        # paragraph("like in interview"),
        heading_2("Solution"),
        # paragraph("your solution here"),
        heading_2("Clarification & Difficulties"),
        # paragraph(" "),
        heading_2("Code"),
        code()


        # Add more blocks as needed
    ]

    payload = {
        'children': block_content
    }

    if not exist:
        endpoint_page_children = f'https://api.notion.com/v1/blocks/{block_id}/children'
        response = requests.patch(endpoint_page_children, json=payload, headers=headers)

        # Get the JSON response
        json_response = response.json()

    # Print the response
    # print(json_response)
    # else:
    #   print('A page with the problem number exists.')

    if not exist:
    # Print the response
        print(json_response)
    else:
        print('A page with the problem number exists.')
