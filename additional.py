"""
Ok, I imagine what this task is about, but without any requirements of 'How' it should be done, what I can is only fix
linting and try to suppose what functions params are about. for better implementation of given task, please add more
requirements.
"""

import re
import datetime


def create_racer_abbreviations_dict(file_name: str) -> dict:
    """
    Retrieves {'abbreviation': (name, team)}" format dict from abbreviations.txt
    :param file_name: name of a file to get data from
    :return dict with parsed file data
    """
    abbreviations_dict = {}
    with open(file_name, 'r') as fn:
        for line in fn:
            match_obj = re.match(r'^(\w+)_([a-zA-Z\s]+)_([a-zA-Z\s]+)$', line)
            # group(1) is abbreviation, i.e 'SVM'
            abbreviations_dict[match_obj.group(1)] = (
                match_obj.group(2),  # name of a pilot
                match_obj.group(3).rstrip(),  # team
            )
    return abbreviations_dict


# {'abbreviation of pilot': ('name of pilot, 'team')}
abbr_dict = create_racer_abbreviations_dict('abbreviations.txt')


def retrieve_timings_from_log(file_name: str) -> dict:
    """
    Get time data from log
    :param file_name
    :return timing log from start.log or end.log in {'abbreviation': time} format
    """
    timing_log = {}
    with open(file_name, 'r') as fn:
        for line in fn:
            # matches 2 groups: abbreviation of a racer and time
            match_obj = re.match(r'^([A-Z]+).*(\d{2}:\d+:\d+\.\d+)$', line)
            # converts time from a string to datetime object
            lap_time = datetime.datetime.strptime(match_obj.group(2).rstrip(), '%H:%M:%S.%f')
            # adds key, value to a timing_log
            timing_log[match_obj.group(1)] = lap_time

    return timing_log


start_timings = retrieve_timings_from_log('start.log')
end_timings = retrieve_timings_from_log('end.log')


def sorted_individual_results(start_timings_: dict, end_timings_: dict, reverse_order: bool = False) -> dict:
    """
    Receives start and end timings and returns an OrderedDict with {abbreviations:timedeltas}
    :param start_timings_:
    :param end_timings_:
    :param reverse_order: direction of values sorting
    :return sorted results
    """
    # creating dict with best lap results
    lap_results = {
        key: end_timings_[key] - start_timings_.get(key, 0) for key in start_timings_.keys()
    }
    sorted_results = dict(sorted(lap_results.items(), key=lambda x: x[1], reverse=reverse_order))

    return sorted_results


sorted_lap_results = sorted_individual_results(start_timings, end_timings)


def print_result_board(sorted_lap_results_: dict):
    """
    Print result board to a console
    :param sorted_lap_results_:
    """
    counter = 1
    for key, value in sorted_lap_results_.items():
        racer_name = abbr_dict[key][0]
        team_name = abbr_dict[key][1]
        best_time = str(value)[2:-3]
        print(("{: <3} {: <18} | {: <30}  | {}".format(str(counter)+'.', racer_name, team_name, best_time)))
        if counter == 15:
            print('----------------------------------------------------------------------')
        counter += 1

