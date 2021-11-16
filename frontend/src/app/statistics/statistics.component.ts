import { Component, OnInit } from '@angular/core';
import { WebService } from '../web.service';

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.css']
})
export class StatisticsComponent implements OnInit {

  players: any = [{id: 1, name: "Fred"}];
  filtered_players_p1: any = [{id: 1, name: "Fred"}]
  filtered_players_p2: any = [{id: 1, name: "Fred"}]
  statistic: any = [];
  vs_statistic: any = [];
  firstInput: number = 0;
  secondInput: number = 0;
  myFilterP1: string = "";
  myFilterP2: string = "";

  constructor(private webService: WebService) {
  }

  getPlayers(): void {
    this.webService.getPlayers()
      .subscribe(players => this.updatePlayers(players));
  }

  updatePlayers(input_players: any)
  {
    this.players = input_players;
    this.filterPlayers();
  }

  filterPlayers()
  {
    var filter: string = this.myFilterP1.toLowerCase();
    var filtered_list: any;
    for (let i = 0; i < 2; i++)
    {
      if (filter == "")
      {
        filtered_list = this.players;
      }
      else
      {
        filtered_list = [];
        for (let player of this.players)
        {
          if (player.name.toLowerCase().includes(filter))
          {
            filtered_list.push(player)
          }
        }
      }

      if (i == 0)
        this.filtered_players_p1 = filtered_list;
      else
        this.filtered_players_p2 = filtered_list;

      filter = this.myFilterP2.toLowerCase();
    }

    if (this.filtered_players_p1.length > 0)
    {
      this.firstInput = this.filtered_players_p1[0].id;
    }
    if (this.filtered_players_p2.length > 0)
    {
      this.secondInput = this.filtered_players_p2[0].id;
    }
  }

  getPlayerStatistics(p1: number): void {
    this.vs_statistic = []
    this.statistic = []
    this.webService.getIndividualStatistics(p1)
        .subscribe(statistic => this.statistic = statistic);
  }

  getVsStatistics(p1: number, p2: number): void {
    this.vs_statistic = []
    this.statistic = []
    this.webService.getMatchStatistics(p1, p2)
        .subscribe(statistic => this.vs_statistic = statistic);
  }

  getPlayerName(id: number): string {
    for (var player of this.players)
    {
      if (player.id == id)
      {
        return player.name;
      }
    }
    return '';
  }

  ngOnInit(): void {
    this.getPlayers();
  }

}
