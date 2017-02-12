"""Models.py - Sets tables in Postgresql database.
Classes - Player, Lineup, Score
"""

from django.db import models
from django.utils import timezone


class Player(models.Model):
    """Describe a player.

    Player attribbutes:
    lineup - the week he is being played
    position - QB, RB, WR, TE, or K
    team - team he plays for
    name - first and last name, just last name, or
           first initial and lastname.
    """

    # A player can be in multiple lineups,
    # but the same player can't be in the
    # same lineup
    lineup = models.ForeignKey(
        'fnfl.Lineup',
        related_name='player',
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=40)

    QUARTERBACK = 'QB'
    RUNNING_BACK = 'RB'
    WIDE_RECEIVER = 'WR'
    TIGHT_END = 'TE'
    KICKER = 'K'
    POSITION_CHOICES = (
        (QUARTERBACK, 'Quarterback'),
        (RUNNING_BACK, 'Running Back'),
        (WIDE_RECEIVER, 'Wide Receiver'),
        (TIGHT_END, 'Tight End'),
        (KICKER, 'Kicker'),
    )

    position = models.CharField(
        max_length=2,
        choices=POSITION_CHOICES,
        default=QUARTERBACK,
    )

    ARIZONA = 'ARI'
    ATLANTA = 'ATL'
    BALTIMORE = 'BAL'
    BUFFALO = 'BUF'
    CAROLINA = 'CAR'
    CHICAGO = 'CHI'
    CINCINATI = 'CIN'
    CLEVELAND = 'CLE'
    DALLAS = 'DAL'
    DENVER = 'DEN'
    DETROIT = 'DET'
    GREEN_BAY = 'GB'
    HOUSTON = 'HOU'
    INDIANAPOLIS = 'IND'
    JACKSONVILLE = 'JAX'
    KANSAS_CITY = 'KC'
    LOS_ANGELES_C = 'LAC'
    LOS_ANGELES_R = 'LAR'
    MIAMI = 'MIA'
    MINNESOTA = 'MINN'
    NEW_ORLEANS = 'NO'
    NEW_ENGLAND = 'NE'
    NEW_YORK_G = 'NYG'
    NEW_YORK_J = 'NYJ'
    OAKLAND = 'OAK'
    PHILIDELPHIA = 'PHI'
    PITTSBURGH = 'PIT'
    SAN_FRANSICO = 'SF'
    SEATTLE = 'SEA'
    TAMPA_BAY = 'TB'
    TENNESSEE = 'TEN'
    WASHINGTON = 'WASH'
    TEAM_CHOICES = (
        (ARIZONA, 'Arizona Cardinals'),
        (ATLANTA, 'Atlanta Falcons'),
        (BALTIMORE, 'Baltimore Ravens'),
        (BUFFALO, 'Buffalo Bills'),
        (CAROLINA, 'Carolina Panthers'),
        (CHICAGO, 'Chicago Bears'),
        (CINCINATI, 'Cincinati Bengals'),
        (CLEVELAND, 'Cleveland Browns'),
        (DALLAS, 'Dallas Cowboys'),
        (DENVER, 'Denver Broncos'),
        (DETROIT, 'Detroit Lions'),
        (GREEN_BAY, 'Green Bay Packers'),
        (HOUSTON, 'Houston Texans'),
        (INDIANAPOLIS, 'Indianapolis Colts'),
        (JACKSONVILLE, 'Jacksonville Jaguars'),
        (KANSAS_CITY, 'Kansas City Chiefs'),
        (LOS_ANGELES_C, 'Los Angeles Chargers'),
        (LOS_ANGELES_R, 'Los Angeles Rams'),
        (MIAMI, 'Miami Dolphins'),
        (MINNESOTA, 'Minnesota Vikings'),
        (NEW_ORLEANS, 'New Orleans Saints'),
        (NEW_ENGLAND, 'New England Patriots'),
        (NEW_YORK_G, 'New York Giants'),
        (NEW_YORK_J, 'New York Jets'),
        (OAKLAND, 'Oakland Raiders'),
        (PHILIDELPHIA, 'Philidelphia Eagles'),
        (PITTSBURGH, 'Pittsburgh Steelers'),
        (SAN_FRANSICO, 'San Fransico 49ers'),
        (SEATTLE, 'Seattle Seahawks'),
        (TAMPA_BAY, 'Tampa Bay Buccaneers'),
        (TENNESSEE, 'Tennessee Titans'),
        (WASHINGTON, 'Washington Redskins'),
    )

    team = models.CharField(
        max_length=4,
        choices=TEAM_CHOICES,
        default=ARIZONA,
    )

    def __str__(self):
        return self.name


class Lineup(models.Model):
    """Describe a Lineup.

    Lineup attributes:
    author - user that's creating a lineup
    week - Week 1 of the season through the
           Super Bowl
    created_date - date the lineup was created
    """

    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )

    WEEK_ONE = 'Week 1'
    WEEK_TWO = 'Week 2'
    WEEK_THREE = 'Week 3'
    WEEK_FOUR = 'Week 4'
    WEEK_FIVE = 'Week 5'
    WEEK_SIX = 'Week 6'
    WEEK_SEVEN = 'Week 7'
    WEEK_EIGHT = 'Week 8'
    WEEK_NINE = 'Week 9'
    WEEK_TEN = 'Week 10'
    WEEK_ELEVEN = 'Week 11'
    WEEK_TWELVE = 'Week 12'
    WEEK_THIRTEEN = 'Week 13'
    WEEK_FOURTEEN = 'Week 14'
    WEEK_FIFTEEN = 'Week 15'
    WEEK_SIXTEEN = 'Week 16'
    WEEK_SEVENTEEN = 'Week 17'
    WEEK_EIGHTEEN = 'Wild Card'
    WEEK_NINETEEN = 'Divisional Round'
    WEEK_TWENTY = 'Conference Championship'
    WEEK_TWENTY_ONE = 'Super Bowl'
    WEEK_CHOICES = (
        (WEEK_ONE, 'Week 1'),
        (WEEK_TWO, 'Week 2'),
        (WEEK_THREE, 'Week 3'),
        (WEEK_FOUR, 'Week 4'),
        (WEEK_FIVE, 'Week 5'),
        (WEEK_SIX, 'Week 6'),
        (WEEK_SEVEN, 'Week 7'),
        (WEEK_EIGHT, 'Week 8'),
        (WEEK_NINE, 'Week 9'),
        (WEEK_TEN, 'Week 10'),
        (WEEK_ELEVEN, 'Week 11'),
        (WEEK_TWELVE, 'Week 12'),
        (WEEK_THIRTEEN, 'Week 13'),
        (WEEK_FOURTEEN, 'Week 14'),
        (WEEK_FIFTEEN, 'Week 15'),
        (WEEK_SIXTEEN, 'Week 16'),
        (WEEK_SEVENTEEN, 'Week 17'),
        (WEEK_EIGHTEEN, 'Wild Card'),
        (WEEK_NINETEEN, 'Divisional Round'),
        (WEEK_TWENTY, 'Conference Championship'),
        (WEEK_TWENTY_ONE, 'Super Bowl'),
    )

    week = models.CharField(
        max_length=24,
        choices=WEEK_CHOICES,
        default=WEEK_ONE,
    )

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.week


class Score(models.Model):
    """Score the player for a given lineup

    Attributes:
    player_to_score - player to score
    lineup_to_score - the week he played
    tds - number of touchdowns
    pass_yds - passing yards
    ints - interceptions thrown
    rush_yds - rushing yards
    rec_yds - receiving yards
    two_pts - number of two point conversions
    fgs - field goals
    xps - extra points
    week_score - the total week scroe

    Methods:
    week_score - calculate the week score
    """
    player_to_score = models.ForeignKey(
        'fnfl.Player',
        related_name='player_to_score',
        on_delete=models.CASCADE,
    )
    lineup_to_score = models.ForeignKey(
        'fnfl.Lineup',
        related_name='lineup_to_score',
        on_delete=models.CASCADE,
    )
    tds = models.IntegerField(default=0)
    pass_yds = models.IntegerField(default=0)
    ints = models.IntegerField(default=0)
    rush_yds = models.IntegerField(default=0)
    rec_yds = models.IntegerField(default=0)
    two_pts = models.IntegerField(default=0)
    fgs = models.IntegerField(default=0)
    xps = models.IntegerField(default=0)

    def _get_name_week(self):
        return '%s %s' % (self.player_to_score, self.lineup_to_score)
    name_week = property(_get_name_week)

    def __str__(self):
        return self.name_week

    def week_score(self):
        """Calculate the week score"""

        total_score = 0
        pass_score = 0
        rush_score = 0
        rec_score = 0

        total_score = (self.tds*6) + \
                      (self.fgs*3) + self.xps + \
                      (self.two_pts*2) - (self.ints*2)

        if self.pass_yds >= 300:
            pass_score = 6 + (int((self.pass_yds-300) / 50) * 3)
        total_score += pass_score

        if self.rush_yds >= 100:
            rush_score = 6 +(int((self.rush_yds-100) / 50) * 3)
        total_score += rush_score

        if self.player_to_score.position == 'WR' and self.rec_yds >= 100:
            rec_score = 6 + (int((self.rec_yds-100) / 50) * 3)

        if self.player_to_score.position != 'WR':
            rec_score = int(self.rec_yds / 50) * 3
        total_score += rec_score

        return total_score

    week_score = property(week_score)
