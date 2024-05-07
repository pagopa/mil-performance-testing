import random

from locust import between
from locust import HttpUser
from locust import task
from util import load_credentials

from src.api import delete_terminal
from src.api import get_paginated_terminals
from src.api import get_terminal_registry_access_token
from src.api import patch_terminal
from src.api import post_new_random_terminal


class Operator(HttpUser):
    wait_time = between(1, 5)

    tr_token_client_id = None
    tr_token_client_secret = None
    access_token_tr = None
    terminals = {}
    active_users = {}

    def on_start(self):
        client_data = load_credentials()

        if 'clients' in client_data:
            for client in client_data['clients']:
                self.tr_token_client_id = client['client_id']
                self.tr_token_client_secret = client['client_secret']
                if (self.tr_token_client_id, self.tr_token_client_secret) not in self.active_users:
                    self.active_users[(self.tr_token_client_id, self.tr_token_client_secret)] = self
                    self.access_token_tr = get_terminal_registry_access_token(self.client, self.tr_token_client_id,
                                                                              self.tr_token_client_secret)
                    self.get_all_terminals()
        else:
            # Quit the test if there are no available clients
            self.environment.runner.quit()

    def on_stop(self):
        self.get_all_terminals()
        while self.terminals:
            self.delete_terminal()
        del self.active_users[(self.tr_token_client_id, self.tr_token_client_secret)]
        self.environment.runner.quit()

    @task(2)
    def get_first_terminals(self):
        response = get_paginated_terminals(self.client, self.access_token_tr, 0)
        assert response.status_code == 200
        for t in response.json()['terminals']:
            self.terminals[t['terminalUuid']] = t

    @task(2)
    def get_all_terminals(self):
        empty = False
        i = 0
        self.terminals = {}

        while not empty:
            response = get_paginated_terminals(self.client, self.access_token_tr, i)
            assert response.status_code == 200
            for t in response.json()['terminals']:
                self.terminals[t['terminalUuid']] = t
            empty = not response.json()['terminals']

            i += 1

    @task(8)
    def create_new_terminal(self):
        response = post_new_random_terminal(self.client, self.access_token_tr)
        assert response.status_code == 201

    @task(3)
    def update_terminal(self):
        if self.terminals:
            target_terminal = random.choice(list(self.terminals.values()))
            target_terminal_uuid = target_terminal['terminalUuid']
            response = patch_terminal(self.client, self.access_token_tr, target_terminal_uuid)
            assert response.status_code == 204

    @task(2)
    def delete_terminal(self):
        if self.terminals:
            target_terminal = random.choice(list(self.terminals.values()))
            target_terminal_uuid = target_terminal['terminalUuid']

            response = delete_terminal(self.client, self.access_token_tr, target_terminal_uuid)
            assert response.status_code == 204
            self.terminals.pop(target_terminal_uuid)
