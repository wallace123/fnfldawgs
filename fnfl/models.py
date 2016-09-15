from django.db import models
from django.utils import timezone

class Player(models.Model):
    lineup = models.ForeignKey(
        'Lineup',
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
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
    DALLAS = 'DAL'
    WASHINGTON = 'WASH'
    NEW_YORK_G = 'NYG'
    PHILIDELPHIA = 'PHI'
    ARIZONA = 'ARI'
    LOS_ANGELES = 'LA'
    SAN_FRANSICO = 'SF'
    SEATTLE = 'SEA'
    CHICAGO = 'CHI'
    DETROIT = 'DET'
    GREEN_BAY = 'GB'
    MINNESOTA = 'MINN'
    ATLANTA = 'ATL'
    CAROLINA = 'CAR'
    NEW_ORLEANS = 'NO'
    TAMPA_BAY = 'TB'
    BUFFALO = 'BUF'
    MIAMI = 'MIA'
    NEW_ENGLAND = 'NE'
    NEW_YORK_J = 'NYJ'
    DENVER = 'DEN'
    KANSAS_CITY = 'KC'
    OAKLAND = 'OAK'
    SAN_DEIGO = 'SD'
    BALTIMORE = 'BAL'
    CINCINATI = 'CIN'
    CLEVELAND = 'CLE'
    PITTSBURGH = 'PIT'
    HOUSTON = 'HOU'
    INDIANAPOLIS = 'IND'
    JACKSONVILLE = 'JAX'
    TENNESSEE = 'TEN'
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
        (LOS_ANGELES, 'Los Angeles Rams'), 
        (MIAMI, 'Miami Dolphins'),
        (MINNESOTA, 'Minnesota Vikings'),
        (NEW_ORLEANS, 'New Orleans Saints'),
        (NEW_ENGLAND, 'New England Patriots'),
        (NEW_YORK_G, 'New York Giants'),
        (NEW_YORK_J, 'New York Jets'),
        (OAKLAND, 'Oakland Raiders'),
        (PHILIDELPHIA, 'Philidelphia Eagles'),
        (PITTSBURGH, 'Pittsburgh Steelers'),
        (SAN_DEIGO, 'San Diego Chargers'),
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

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)

    def __str__(self):
        return '%s %s' % (self.full_name, self.lineup)

class Lineup(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    WEEK_ONE = '1'
    WEEK_TWO = '2'
    WEEK_THREE = '3'
    WEEK_FOUR = '4'
    WEEK_FIVE = '5'
    WEEK_SIX = '6'
    WEEK_SEVEN = '7'
    WEEK_EIGHT = '8'
    WEEK_NINE = '9'
    WEEK_TEN = '10'
    WEEK_ELEVEN = '11'
    WEEK_TWELVE = '12'
    WEEK_THIRTEEN = '13'
    WEEK_FOURTEEN = '14'
    WEEK_FIFTEEN = '15'
    WEEK_SIXTEEN = '16'
    WEEK_SEVENTEEN = '17'
    WILD_CARD = '18'
    DIVISIONAL_ROUND = '19'
    CONFERENCE_CHAMPIONSHIP = '20'
    SUPER_BOWL = '21'
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
        (WILD_CARD, 'Wild Card'),
        (DIVISIONAL_ROUND, 'Divisional Round'),
        (CONFERENCE_CHAMPIONSHIP, 'Conference Championship'),
        (SUPER_BOWL, 'Super Bowl'),
    )
    week = models.CharField(
        max_length=2,
        choices=WEEK_CHOICES,
        default=WEEK_ONE,
    )

    qb_position = models.CharField(max_length=2, default='QB')
    qb_first_name = models.CharField(max_length=20)
    qb_last_name = models.CharField(max_length=20)
    qb_team = models.CharField(
        max_length=4,
        choices=Player.TEAM_CHOICES,
        default=Player.ARIZONA,
    )

    rb1_position = models.CharField(max_length=2, default='RB')
    rb1_first_name = models.CharField(max_length=20)
    rb1_last_name = models.CharField(max_length=20)
    rb1_team = models.CharField(
        max_length=4,
        choices=Player.TEAM_CHOICES,
        default=Player.ARIZONA,
    )

    rb2_position = models.CharField(max_length=2, default='RB')
    rb2_first_name = models.CharField(max_length=20)
    rb2_last_name = models.CharField(max_length=20)
    rb2_team = models.CharField(
        max_length=4,
        choices=Player.TEAM_CHOICES,
        default=Player.ARIZONA,
    )

    wr1_position = models.CharField(max_length=2, default='WR')
    wr1_first_name = models.CharField(max_length=20)
    wr1_last_name = models.CharField(max_length=20)
    wr1_team = models.CharField(
        max_length=4,
        choices=Player.TEAM_CHOICES,
        default=Player.ARIZONA,
    )

    wr2_position = models.CharField(max_length=2, default='WR')
    wr2_first_name = models.CharField(max_length=20)
    wr2_last_name = models.CharField(max_length=20)
    wr2_team = models.CharField(
        max_length=4,
        choices=Player.TEAM_CHOICES,
        default=Player.ARIZONA,
    )

    te_position = models.CharField(max_length=2, default='TE')
    te_first_name = models.CharField(max_length=20)
    te_last_name = models.CharField(max_length=20)
    te_team = models.CharField(
        max_length=4,
        choices=Player.TEAM_CHOICES,
        default=Player.ARIZONA,
    )

    k_position = models.CharField(max_length=2, default='K')
    k_first_name = models.CharField(max_length=20)
    k_last_name = models.CharField(max_length=20)
    k_team = models.CharField(
        max_length=4,
        choices=Player.TEAM_CHOICES,
        default=Player.ARIZONA,
    )

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.week

class Score(models.Model):
    player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE,
    )
    lineup_week = models.ForeignKey(
        'Lineup',
        on_delete=models.CASCADE,
    )
    tds = models.IntegerField(default=0)
    pass_yds = models.IntegerField(default=0)
    ints = models.IntegerField(default=0)
    rush_yds = models.IntegerField(default=0)
    rec_yds = models.IntegerField(default=0)
    ret_tds = models.IntegerField(default=0)
    two_pts = models.IntegerField(default=0)
    fgs = models.IntegerField(default=0)
    xps = models.IntegerField(default=0)

    def _get_name_week(self):
        return '%s %s' % (self.player, self.lineup_week)
    name_week = property(_get_name_week)

    def __str__(self):
        return self.name_week

    def week_score(self):
        total_score = 0
        pass_score = 0
        rush_score = 0
        rec_score = 0

        total_score = (self.tds*6) + (self.ret_tds*6) + \
                      (self.fgs*3) + self.xps + \
                      (self.two_pts*2) - (self.ints*2)

        if (self.pass_yds >= 300):
            pass_score = 6 + (int((self.pass_yds-300) / 50) * 3)
        total_score += pass_score

        if (self.rush_yds >= 100):
            rush_score = 6 +(int((self.rush_yds-100) / 50) * 3)
        total_score += rush_score

        if (self.player.position == 'WR' and self.rec_yds >= 100):
            rec_score = 6 + (int((self.rec_yds-100) / 50) * 3)

        if (self.player.position != 'WR'):
            rec_score = int(self.rec_yds / 50) * 3
        total_score += rec_score

        return total_score
    week_score = property(week_score)
