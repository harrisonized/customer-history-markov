import datetime as dt
import numpy as np
import pandas as pd
from .data import truncate_timestamp, uniform_random_timestamp


class Customer:
    order_num = 0
    max_order_num = 4  # stop recording after 5 rows
    
    # generate timestamps
    earliest_start = dt.datetime(2020, 11, 24, 10, 15, 0)
    latest_start = dt.datetime(2020, 11, 24, 12, 0, 0)

    # starting conditions
    choices = ['Space Mountain', 'Indiana Jones Adventure', 'Haunted Mansion']
    initial_weights = [0.50, 0.30, 0.20]

    # model parameters
    env_start = dt.datetime(2020, 11, 24, 10, 0, 0)
    transition_matrix = pd.DataFrame(
        [[0.8, 0.15, 0.05],
         [0.3, 0.65, 0.05],
         [0.15, 0.05, 0.8]],
        index=self.choices,
        columns=self.choices,
    )
    wait_times = [65, 44, 23]
    dropout_rates = [0.9, 0.3, 0.8]

    def __init__(self, env, results, customer_id):
        self.env = env
        self.results = results
        self.customer_id = customer_id
        self.current_time = truncate_timestamp(self.first_timestamp())
        self.current_choice = self.first_choice()
        self.is_active = True        

    def make_choices(self):
        """Customer makes a choice, then the event is recorded
        Customer may drop out
        If customer is still active, customer makes the next choice then waits     
        """
        
        yield self.align_env_clock()
        
        while self.is_active & (self.order_num <= self.max_order_num):
            
            # record the result
            self.results.append({'customer_id': self.customer_id,
                                 'order_num': self.order_num,
                                 'order_date': self.current_time,
                                 'item': self.current_choice})
            
            # customer may drop out
            self.is_active = self.stay_active()
            
            # make next choice
            if self.is_active:
                self.order_num += 1
                self.current_choice = self.next_choice()
                yield self.wait()
                self.current_time = truncate_timestamp(self.generate_timestamp())

    def align_env_clock(self):
        return self.env.timeout(
            (self.current_time-self.env_start).seconds/60
        )
    
    def first_timestamp(self):
        return uniform_random_timestamp(self.earliest_start, self.latest_start)
    
    def generate_timestamp(self):
        return self.env_start+dt.timedelta(minutes=self.env.now)    
    
    def first_choice(self):
        return np.random.choice(self.choices, p=self.initial_weights)
    
    def next_choice(self):
        """ choose based on previous choice """
        return self.transition_matrix.loc[self.current_choice].sample(
            weights=self.transition_matrix.loc[self.current_choice]).index[0]

    def stay_active(self):
        idx = self.choices.index(self.current_choice)
        dropout_rate = self.dropout_rates[idx]
        return np.random.choice([False, True], p=[dropout_rate, 1-dropout_rate])

    def wait(self):
        """ duration in minutes """
        idx = self.choices.index(self.current_choice)
        walk_time = np.random.poisson(10)  # walk to the next ride
        wait_time = np.random.poisson(self.wait_times[idx])  # wait for the next ride
        return self.env.timeout(walk_time+wait_time)
