import datetime as dt
import numpy as np


# Functions included in this file:
# # title_case_to_initials
# # sort_df
# # truncate_timestamp
# # uniform_random_timestmap


def title_case_to_initials(text):
    """Converts "Column Title" to CT
    """
    return ''.join([word[0].upper() for word in text.split()])


def sort_df(df, col: list, row:list):
    """Convenience function """
    return df.loc[row, col]


def truncate_timestamp(timestamp):
    return timestamp.replace(microsecond=0)


def uniform_random_timestamp(start, end, timescale='minutes'):
    """Randomly picks a timestamp between start and end
    Uses the uniform distribution
    """

    if timescale == 'minutes':
        return start + dt.timedelta(
            minutes = np.random.uniform(0, (end-start).seconds/60)
        )

    if timescale == 'days':
        return start + dt.timedelta(
            days = np.random.uniform(0, (end-start).days)
        )
