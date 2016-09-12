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
        (DALLAS, 'Dallas Cowboys'),
        (WASHINGTON, 'Washington Redskins'),
        (NEW_YORK_G, 'New York Giants'),
        (PHILIDELPHIA, 'Philidelphia Eagles'),
        (ARIZONA, 'Arizona Cardinals'),
        (LOS_ANGELES, 'Los Angeles Rams'), 
        (SAN_FRANSICO, 'San Fransico 49ers'),
        (SEATTLE, 'Seattle Seahawks'),
        (CHICAGO, 'Chicago Bears'),
        (DETROIT, 'Detroit Lions'),
        (GREEN_BAY, 'Green Bay Packers'),
        (MINNESOTA, 'Minnesota Vikings'),
        (ATLANTA, 'Atlanta Falcons'),
        (CAROLINA, 'Carolina Panthers'),
        (NEW_ORLEANS, 'New Orleans Saints'),
        (TAMPA_BAY, 'Tampa Bay Buccaneers'),
        (BUFFALO, 'Buffalo Bills'),
        (MIAMI, 'Miami Dolphins'),
        (NEW_ENGLAND, 'New England Patriots'),
        (NEW_YORK_J, 'New York Jets'),
        (DENVER, 'Denver Broncos'),
        (KANSAS_CITY, 'Kansas City Chiefs'),
        (OAKLAND, 'Oakland Raiders'),
        (SAN_DEIGO, 'San Diego Chargers'),
        (BALTIMORE, 'Baltimore Ravens'),
        (CINCINATI, 'Cincinati Bengals'),
        (CLEVELAND, 'Clevland Browns'),
        (PITTSBURGH, 'Pittsburgh Steelers'),
        (HOUSTON, 'Houston Texans'),
        (INDIANAPOLIS, 'Indianapolis Colts'),
        (JACKSONVILLE, 'Jacksonville Jaguars'),
        (TENNESSEE, 'Tennessee Titans'),
    )
    team = models.CharField(
        max_length=4,
        choices=TEAM_CHOICES,
        default=DALLAS,
    )

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)

    def __str__(self):
        return self.full_name

class Lineup(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    week = models.CharField(max_length=50)
    qb = models.CharField(max_length=50)
    rb1 = models.CharField(max_length=50)
    rb2 = models.CharField(max_length=50)
    wr1 = models.CharField(max_length=50)
    wr2 = models.CharField(max_length=50)
    te = models.CharField(max_length=50)
    k = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.week
