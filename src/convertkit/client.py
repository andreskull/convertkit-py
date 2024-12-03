import requests
import numpy as np
from .exceptions import ConvertKitAPIError

class ConvertKit:
    BASE_URL = "https://api.convertkit.com/v3"
    
    def __init__(self, api_key, api_secret, form_name=None):
        """
        Initialize ConvertKit client with API credentials.
        
        Args:
            api_key (str): Public API key
            api_secret (str): Secret API key
            form_id (str): Form ID
        """
        self.api_key = api_key
        self.api_secret = api_secret
        if form_name:
            self.form_id = self.get_form_id_by_name(form_name)
            if not self.form_id:
                print(f"Form '{form_name}' not found. Available forms:")
    
    def list_custom_fields(self):
        """
        List all custom fields in the account.
        
        Returns:
            list: List of custom field objects
        """
        url = f"{self.BASE_URL}/custom_fields"
        params = {'api_key': self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('custom_fields', [])
        else:
            response.raise_for_status()
    
    def create_custom_fields(self, labels):
        """
        Create new custom fields if they don't already exist.
        
        Args:
            labels (list): List of labels for new custom fields
        """
        existing_fields = self.list_custom_fields()
        existing_labels = {field['label'] for field in existing_fields}
        
        new_labels = [label for label in labels if label not in existing_labels]
        if not new_labels:
            print("No new custom fields to create.")
            return
        
        url = f"{self.BASE_URL}/custom_fields"
        headers = {'Content-Type': 'application/json'}
        data = {
            'api_secret': self.api_secret,
            'label': new_labels
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Custom fields created successfully.")
        else:
            response.raise_for_status()
            
    def list_tags(self):
        """
        List all tags in the account.
        
        Returns:
            list: List of tag objects containing id, name, and created_at
        """
        url = f"{self.BASE_URL}/tags"
        params = {'api_key': self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('tags', [])
        else:
            response.raise_for_status()

    def create_tags(self, tag_names):
        """
        Create new tags if they don't already exist.
        
        Args:
            tag_names (list): List of tag names to create
            
        Returns:
            list: List of created tag objects
        """
        if not isinstance(tag_names, list):
            tag_names = [tag_names]
            
        # Get existing tags to avoid duplicates
        existing_tags = self.list_tags()
        existing_names = {tag['name'] for tag in existing_tags}
        
        # Filter out tags that already exist
        new_tags = [name for name in tag_names if name not in existing_names]
        if not new_tags:
            print("No new tags to create.")
            return []
        
        # Create new tags
        url = f"{self.BASE_URL}/tags"
        headers = {'Content-Type': 'application/json'}
        data = {
            'api_secret': self.api_secret,
            'tag': [{'name': tag_name} for tag_name in new_tags]
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Tags created successfully.")
            return response.json()
        else:
            print("Failed to create tags.")
            response.raise_for_status()
            
    def list_subscribers(self, page=1, from_date=None, to_date=None, updated_from=None, 
                    updated_to=None, sort_order='asc', sort_field=None, email_address=None):
        """
        List subscribers with pagination and optional filters.
        
        Args:
            page (int): Page number, default 1. Each page contains up to 50 subscribers.
            from_date (str): Filter subscribers added on or after this date (format: yyyy-mm-dd)
            to_date (str): Filter subscribers added on or before this date (format: yyyy-mm-dd)
            updated_from (str): Filter subscribers updated after this date (format: yyyy-mm-dd)
            updated_to (str): Filter subscribers updated before this date (format: yyyy-mm-dd)
            sort_order (str): Sort order for results ('asc' or 'desc')
            sort_field (str): Field to sort by (currently only 'cancelled_at' is supported)
            email_address (str): Search subscribers by email address
        
        Returns:
            dict: Response containing total_subscribers, page, total_pages, and subscribers list
        """
        url = f"{self.BASE_URL}/subscribers"
        
        # Build parameters
        params = {
            'api_secret': self.api_secret,
            'page': page
        }
        
        # Add optional parameters if provided
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        if updated_from:
            params['updated_from'] = updated_from
        if updated_to:
            params['updated_to'] = updated_to
        if sort_order and sort_order.lower() in ['asc', 'desc']:
            params['sort_order'] = sort_order.lower()
        if sort_field:
            params['sort_field'] = sort_field
        if email_address:
            params['email_address'] = email_address
            
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def list_all_subscribers(self, from_date=None, to_date=None, updated_from=None, 
                            updated_to=None, sort_order='asc', sort_field=None, email_address=None):
        """
        List all subscribers by handling pagination automatically.
        
        Args:
            Same as list_subscribers except 'page'
        
        Returns:
            list: Complete list of all subscribers
        """
        all_subscribers = []
        page = 1
        
        while True:
            response = self.list_subscribers(
                page=page,
                from_date=from_date,
                to_date=to_date,
                updated_from=updated_from,
                updated_to=updated_to,
                sort_order=sort_order,
                sort_field=sort_field,
                email_address=email_address
            )
            
            subscribers = response.get('subscribers', [])
            all_subscribers.extend(subscribers)
            
            # Check if we've reached the last page
            if page >= response.get('total_pages', 0):
                break
                
            page += 1
        
        return all_subscribers
    
    def list_subscriber_tags(self, subscriber_id):
        """
        List all tags for a specific subscriber.
        
        Args:
            subscriber_id (int): The ID of the subscriber.
        
        Returns:
            list: List of tag objects for the subscriber.
        """
        url = f"{self.BASE_URL}/subscribers/{subscriber_id}/tags"
        params = {'api_key': self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('tags', [])
        else:
            response.raise_for_status()

    def list_subscribers_with_tags(self, page=1, from_date=None, to_date=None, updated_from=None, 
                                updated_to=None, sort_order='asc', sort_field=None, email_address=None):
        """
        List subscribers with their tags.
        
        Args:
            Same as list_subscribers.
        
        Returns:
            list: List of subscriber objects with their tags.
        """
        subscribers = self.list_subscribers(
            page=page,
            from_date=from_date,
            to_date=to_date,
            updated_from=updated_from,
            updated_to=updated_to,
            sort_order=sort_order,
            sort_field=sort_field,
            email_address=email_address
        ).get('subscribers', [])
        
        for subscriber in subscribers:
            subscriber_id = subscriber.get('id')
            subscriber['tags'] = self.list_subscriber_tags(subscriber_id)
        
        return subscribers
    
    def get_subscriber(self, subscriber_id):
        """
        Get subscriber details by ID using list_all_subscribers.
        
        Args:
            subscriber_id (int): The subscriber's ID
            
        Returns:
            dict: Subscriber details if found, None if not found
        """
        subscribers = self.list_all_subscribers()
        for subscriber in subscribers:
            if subscriber['id'] == subscriber_id:
                print(f"Found subscriber {subscriber_id}: {subscriber}")  # Debug info
                return subscriber
        print(f"Subscriber {subscriber_id} not found")
        return None
    
    def create_subscriber_with_fields_and_tags(self, subscriber_data):
        """
        Add a subscriber to a form with custom fields and tags.
        
        Args:
            subscriber_data (dict): Dictionary containing email, fields, and tags
        """
        url = f"{self.BASE_URL}/forms/{self.form_id}/subscribe"
        
        # Convert numpy array to list if needed and handle None
        tag_names = []
        if 'tags' in subscriber_data:
            if isinstance(subscriber_data['tags'], np.ndarray):
                tag_names = subscriber_data['tags'].tolist()
            elif isinstance(subscriber_data['tags'], list):
                tag_names = subscriber_data['tags']
        
        # Get tag IDs for the tag names
        tag_ids = []
        for tag_name in tag_names:
            tag_id = self.get_tag_id_by_name(tag_name)
            if tag_id:
                tag_ids.append(tag_id)
            
        data = {
            'api_key': self.api_key,
            'email': subscriber_data['email'],
            'fields': subscriber_data['fields'],
            'tags': tag_ids  # Send tag IDs instead of names
        }  
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            subscriber_id = response.json()['subscription']['subscriber']['id']
            print(f"Subscriber {subscriber_data['email']} added with ID: {subscriber_id}")
        else:
            response.raise_for_status()

    def update_subscriber_fields_and_tags(self, subscriber_id, update_data):
        """
        Update subscriber's custom fields and tags.
        
        Args:
            subscriber_id (int): The subscriber's ID
            update_data (dict): Dictionary containing fields and tags to update
        """
        # Update fields
        url = f"{self.BASE_URL}/subscribers/{subscriber_id}"
        data = {
            'api_secret': self.api_secret,
            'fields': update_data['fields']
        }
        
        response = requests.put(url, json=data)
        if response.status_code != 200:
            response.raise_for_status()
            
        # Ensure tags are a list
        tags = []
        if 'tags' in update_data:
            if isinstance(update_data['tags'], np.ndarray):
                tags = update_data['tags'].tolist()
            elif isinstance(update_data['tags'], list):
                tags = update_data['tags']
        
        # Update tags
        current_tags = set(tag['name'] for tag in self.list_subscriber_tags(subscriber_id))
        new_tags = set(update_data['tags'])
        
        # Add missing tags
        tags_to_add = new_tags - current_tags
        if tags_to_add:
            self.add_tags_to_subscriber(subscriber_id, list(tags_to_add))
        
        # Remove extra tags
        tags_to_remove = current_tags - new_tags
        if tags_to_remove:
            self.remove_tags_from_subscriber(subscriber_id, list(tags_to_remove))

    def get_tag_id_by_name(self, tag_name):
        """
        Get tag ID by its name.
        
        Args:
            tag_name (str): Name of the tag
            
        Returns:
            int: Tag ID if found, None if not found
        """
        tags = self.list_tags()
        for tag in tags:
            if tag['name'].lower() == tag_name.lower():
                return tag['id']
        print(f"Tag '{tag_name}' not found")
        return None

    def add_tags_to_subscriber(self, subscriber_id, tag_names):
        """
        Add tags to a subscriber.
        
        Args:
            subscriber_id (int): The subscriber's ID
            tag_names (list): List of tag names to add
        """
        # First get subscriber's email
        subscriber = self.get_subscriber(subscriber_id)
        if not subscriber:
            print(f"Subscriber {subscriber_id} not found")
            return
            
        subscriber_email = subscriber.get('email_address')
        
        for tag_name in tag_names:
            tag_id = self.get_tag_id_by_name(tag_name)
            if tag_id:
                url = f"{self.BASE_URL}/tags/{tag_id}/subscribe"
                data = {
                    'api_secret': self.api_secret,
                    'email': subscriber_email
                }
                
                response = requests.post(url, json=data)
                if response.status_code != 200:
                    print(f"Error adding tag '{tag_name}' to subscriber {subscriber_email}: {response.text}")
                    response.raise_for_status()
                else:
                    print(f"Added tag '{tag_name}' to subscriber {subscriber_email}")
            else:
                print(f"Skipping tag '{tag_name}' as it doesn't exist")

    def remove_tags_from_subscriber(self, subscriber_id, tag_names):
        """
        Remove tags from a subscriber.
        
        Args:
            subscriber_id (int): The subscriber's ID
            tag_names (list): List of tag names to remove
        """
        # First get subscriber's email
        subscriber = self.get_subscriber(subscriber_id)
        if not subscriber:
            print(f"Subscriber {subscriber_id} not found")
            return
            
        subscriber_email = subscriber.get('email_address')
        
        for tag_name in tag_names:
            tag_id = self.get_tag_id_by_name(tag_name)
            if tag_id:
                url = f"{self.BASE_URL}/tags/{tag_id}/unsubscribe"
                data = {
                    'api_secret': self.api_secret,
                    'email': subscriber_email
                }
                
                response = requests.post(url, json=data)  # Note: it's POST, not DELETE
                if response.status_code != 200:
                    print(f"Error removing tag '{tag_name}' from subscriber {subscriber_email}: {response.text}")
                    response.raise_for_status()
                else:
                    print(f"Removed tag '{tag_name}' from subscriber {subscriber_email}")
            else:
                print(f"Skipping tag '{tag_name}' as it doesn't exist")
                
    def list_forms(self):
        """
        List all forms in the account.
        
        Returns:
            list: List of form objects containing id, name, type, and other attributes
        """
        url = f"{self.BASE_URL}/forms"
        params = {'api_key': self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('forms', [])
        else:
            response.raise_for_status()
            
    def get_form_id_by_name(self, form_name):
        """
        Get form ID by its name.
        
        Args:
            form_name (str): Name of the form to find
            
        Returns:
            int: Form ID if found
            None: If no form with given name exists
        """
        forms = self.list_forms()
        
        for form in forms:
            if form['name'].lower() == form_name.lower():
                return form['id']
            
        print(f"Form '{form_name}' not found. Available forms:")
        for form in forms:
            print(f"- {form['name']}")
        return None

