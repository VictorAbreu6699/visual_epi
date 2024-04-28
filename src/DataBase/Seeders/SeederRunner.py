from src.DataBase.Seeders.CitySeeder import CitySeeder
from src.DataBase.Seeders.RegionSeeder import RegionSeeder
from src.DataBase.Seeders.StateSeeder import StateSeeder


class SeederRunner:

    @staticmethod
    def run():
        RegionSeeder.run()
        StateSeeder.run()
        CitySeeder.run()

