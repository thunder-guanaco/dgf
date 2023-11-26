import logging
from abc import abstractmethod, ABC
from datetime import datetime

import requests

from dgf import external_user_finder
from dgf.models import Tournament, Attendance, Tour, Division, Result
from dgf_cms.settings import DISC_GOLF_METRIX_COMPETITION_ENDPOINT, DISC_GOLF_METRIX_DATE_FORMAT

logger = logging.getLogger(__name__)


class DiscGolfMetrixImporter(ABC):

    @property
    @abstractmethod
    def root_id(self):
        ...

    @property
    @abstractmethod
    def point_system(self):
        ...

    @property
    @abstractmethod
    def divisions(self):
        ...

    @abstractmethod
    def extract_name(self, dgm_tournament):
        ...

    @abstractmethod
    def generate_tours(self, tournament):
        ...

    def get_tournament(self, id):
        url = DISC_GOLF_METRIX_COMPETITION_ENDPOINT.format(id)
        logger.info(f'GET {url}')
        return requests.get(url).json()['Competition']

    def get_results(self, dgm_tournament):
        try:
            return dgm_tournament['TourResults']
        except KeyError:
            return dgm_tournament['SubCompetitions'][0]['Results']

    def get_position(self, dgm_result):
        try:
            return dgm_result['Place']
        except KeyError:
            return dgm_result['OrderNumber']

    def get_division(self, dgm_result):
        dgm_class = dgm_result.get('ClassName') or 'Open'
        return Division.objects.get(id=self.divisions[dgm_class])

    def add_attendance(self, tournament, dgm_tournament):
        for dgm_result in self.get_results(dgm_tournament):
            friend = external_user_finder.find_friend(dgm_result['UserID'], dgm_result['Name'])
            logger.info(f'Using Friend: {friend}')
            _, created = Attendance.objects.get_or_create(friend=friend, tournament=tournament)
            if created:
                logger.info(f'Added attendance of {friend} to {tournament}\n')

    def create_result(self, dgm_result, division, friend, tournament):
        return Result.objects.create(tournament=tournament,
                                     friend=friend,
                                     position=self.get_position(dgm_result),
                                     division=division)

    def add_results(self, tournament, dgm_tournament):
        for dgm_result in self.get_results(dgm_tournament):
            friend = external_user_finder.find_friend(dgm_result['UserID'], dgm_result['Name'])
            logger.info(f'Using Friend: {friend}')
            division = self.get_division(dgm_result)
            result = self.create_result(dgm_result, division, friend, tournament)
            logger.info(f'Added result: {result}')

    def add_or_update_tournament(self, dgm_tournament):
        name = self.extract_name(dgm_tournament)
        date = datetime.strptime(dgm_tournament['Date'], DISC_GOLF_METRIX_DATE_FORMAT)
        dgm_id = dgm_tournament['ID']

        tournament, created = Tournament.objects.get_or_create(metrix_id=dgm_id,
                                                               defaults={
                                                                   'name': name,
                                                                   'begin': date,
                                                                   'end': date,
                                                                   'point_system': self.point_system,
                                                               })

        if created:
            logger.info(f'Created tournament {tournament}\n')
        else:
            # Always update, the dates might have changed and the name changes after the tournament
            tournament.name = name
            tournament.begin = date
            tournament.end = date
            tournament.save()

        return tournament

    def add_to_tour(self, name, tournament, divisions, evaluate_how_many):
        for division in divisions:
            tour, created = Tour.objects.get_or_create(name=name,
                                                       division=Division.objects.get(id=division),
                                                       defaults={'evaluate_how_many': evaluate_how_many})

            if created:
                logger.info(f'Created Tour: {tour}')

            tournament.tours.add(tour)
            logger.info(f'Added {tournament} to {tour}')

    def add_tours(self, tournament):
        divisions = tournament.results.filter(division__isnull=False).values_list('division', flat=True).distinct()

        if not divisions:
            logger.info(f'Skipping adding tours to {tournament.name} because it has no results (and no divisions)')
            return

        for name, evaluate_how_many in self.generate_tours(tournament):
            self.add_to_tour(name, tournament, divisions, evaluate_how_many)

    def create_or_update_tournament(self, metrix_id):

        dgm_tournament = self.get_tournament(metrix_id)
        tournament = self.add_or_update_tournament(dgm_tournament)

        # tournament is either not played yet or still in play
        if tournament.begin >= datetime.today():
            self.add_attendance(tournament, dgm_tournament)

        # tournament was already played and does not have results
        elif tournament.results.count() == 0:
            self.add_results(tournament, dgm_tournament)
            tournament.recalculate_points()

        self.add_tours(tournament)

    def get_tournaments(self, dgm_tournament):
        try:
            return dgm_tournament['Events']
        except KeyError:
            return dgm_tournament['SubCompetitions']

    def update_tournaments(self):
        dgm_tournament = self.get_tournament(self.root_id)
        for dgm_event in self.get_tournaments(dgm_tournament):
            if not dgm_event['Name'].startswith('[DELETED]'):
                logger.info('\n')
                self.create_or_update_tournament(dgm_event['ID'])
                logger.info('--------------------------------------------------------------------------------')


def next_tournaments(name):
    return Tournament.objects.filter(name__startswith=name) \
        .filter(begin__gte=datetime.today()) \
        .order_by('begin')
